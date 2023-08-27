import datetime
from pydantic import BaseModel, field_serializer


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

    @field_serializer('date')
    def serialize_date(self, date: datetime.date, _info):
        return date.strftime("%B %d, %Y")
