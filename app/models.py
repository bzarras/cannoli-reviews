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
    img_url: str
    tags: list[str] = []

    # not working for some reason
    @property
    def pretty_date(self):
        return self.date.strftime("%B %d, %Y")
