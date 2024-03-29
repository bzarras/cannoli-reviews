import datetime
from sqlalchemy import (
    BLOB,
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
)

from app.db import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    data = Column(BLOB)
    etag = Column(String)
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    date = Column(String)
    slug = Column(String, index=True)
    summary = Column(String)
    liked = Column(String)
    disliked = Column(String)
    rating = Column(Float)
    img_url = Column(String)
    visible = Column(Boolean, default=True)
    link = Column(String)
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
