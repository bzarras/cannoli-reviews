from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import tables, models


def get_image_names(db: Session) -> list[str]:
    names = db.scalars(
        statement=select(tables.Image.name)
    )
    return names


def get_image_by_name(db: Session, name: str) -> Optional[models.Image]:
    image = db.scalars(
        statement=select(tables.Image).where(tables.Image.name == name)
    ).first()
    return models.Image.model_validate(image) if image else None


def create_image(db: Session, image: models.ImageCreate) -> tables.Image:
    db_image = tables.Image(name=image.name, data=image.data, etag=image.etag)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

