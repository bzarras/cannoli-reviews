import datetime
from pydantic import BaseModel


class Review(BaseModel):
    title: str
    location: str
    date: datetime.date
    slug: str
    summary: str
    liked: str
    disliked: str
    rating: float
    tags: list[str] = []
