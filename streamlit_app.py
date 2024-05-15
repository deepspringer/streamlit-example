import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class ArticleGroup(Base):
    __tablename__ = 'article_group'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    link = Column(String)
    headlines = Column(String)
    group_id = Column(Integer, ForeignKey('article_group.id'))
    group = relationship("ArticleGroup", back_populates="articles")

ArticleGroup.articles = relationship("Article", order_by=Article.id, back_populates="group")

# Create an engine that stores data in the local directory's
engine = create_engine('sqlite:///articles.db')
Base.metadata.create_all(engine)


"""
# Welcome to Streamlit!

This is J

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

indices = np.linspace(0, 1, num_points)
theta = 2 * np.pi * num_turns * indices
radius = indices

x = radius * np.cos(theta)
y = radius * np.sin(theta)

df = pd.DataFrame({
    "x": x,
    "y": y,
    "idx": indices,
    "rand": np.random.randn(num_points),
})

st.altair_chart(alt.Chart(df, height=700, width=700)
    .mark_point(filled=True)
    .encode(
        x=alt.X("x", axis=None),
        y=alt.Y("y", axis=None),
        color=alt.Color("idx", legend=None, scale=alt.Scale()),
        size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
    ))

import streamlit as st
from sqlalchemy.orm import sessionmaker
import random

# Database session setup
Session = sessionmaker(bind=engine)
session = Session()

def get_random_articles():
    groups = session.query(ArticleGroup).all()
    if not groups:
        return []
    group = random.choice(groups)
    articles = group.articles
    random.shuffle(articles)
    return [(article.headlines.split('|')[i % 4], article.text, article.link) for i, article in enumerate(articles)]

def display_articles():
    st.header("Explore Random Articles")
    articles = get_random_articles()
    if not articles:
        st.write("No articles found. Please check the database.")
        return
    for headline, text, link in articles:
        with st.expander(f"Read about: {headline}"):
            st.write(text)
            st.markdown(f"[Read more]({link})", unsafe_allow_html=True)

def main():
    st.title('Welcome to the Streamlit Article Explorer')
    display_articles()

if __name__ == "__main__":
    main()

