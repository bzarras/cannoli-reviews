import datetime
from pydantic import BaseModel, computed_field, field_serializer


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

    @computed_field
    @property
    def badge_color(self) -> str:
        if self.rating >= 9.0:
            return "#3DA13D"
        elif self.rating >= 8.0:
            return "#78CC78"
        elif self.rating >= 7.0:
            return "#FFE536"
        elif self.rating >= 6.0:
            return "#FFF29C"
        else:
            return "#FF5368"

    @field_serializer('date')
    def serialize_date(self, date: datetime.date, _info):
        return date.strftime("%B %d, %Y")
