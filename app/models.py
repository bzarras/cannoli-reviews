import datetime
from typing import Optional
from pydantic import (
    BaseModel,
    ConfigDict,
    computed_field,
    Field,
    field_serializer,
)


class ImageBase(BaseModel):
    name: str
    data: bytes
    etag: str


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime = Field(exclude=True)
    updated_at: datetime.datetime = Field(exclude=True)

    @computed_field
    @property
    def type(self) -> str:
        _, extension = self.name.split(".")
        ext_lower = extension.lower()
        if ext_lower in ["jpg", "jpeg"]:
            return "jpeg"
        elif ext_lower == "png":
            return "png"
        else:
            raise ValueError("image doesn't have a valid type")


class ReviewBase(BaseModel):
    title: str
    location: str
    latitude: float
    longitude: float
    date: datetime.date
    slug: str
    summary: str
    liked: str
    disliked: str
    rating: float
    img_url: str
    link: str
    visible: bool = True


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    id: int


class Review(ReviewBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime = Field(exclude=True)
    updated_at: datetime.datetime = Field(exclude=True)

    @computed_field
    @property
    def badge_color(self) -> str:
        if self.rating >= 9.0:
            return "#3EB489"  # Mint
        elif self.rating >= 8.0:
            return "#78CC78"
        elif self.rating >= 7.0:
            return "#B2C248"  # Avocado Green
        elif self.rating >= 6.0:
            return "#FAF884"  # Pastel Yellow
        else:
            return "#F08080"  # LightCoral

    @field_serializer('date')
    def serialize_date(self, date: datetime.date, _info):
        return date.strftime("%B %d, %Y")
