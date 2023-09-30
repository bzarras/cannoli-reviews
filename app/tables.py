from sqlalchemy import BLOB, Boolean, Column, Float, Integer, String

from app.db import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    data = Column(BLOB)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    location = Column(String)
    date = Column(String)
    slug = Column(String, index=True)
    summary = Column(String)
    liked = Column(String)
    disliked = Column(String)
    rating = Column(Float)
    img_url = Column(String)
    visible = Column(Boolean, default=True)
    link = Column(String)
