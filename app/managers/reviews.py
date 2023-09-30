from typing import Optional, Union
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import tables, models


def get_all_reviews(db: Session, order_by: Optional[str] = None) -> list[models.Review]:
    order = (
        tables.Review.rating.desc()
        if order_by == "rating"
        else tables.Review.date.desc()
    )
    db_reviews = db.scalars(
        select(tables.Review).order_by(order)
    )
    return [models.Review.model_validate(dbr) for dbr in db_reviews]


def get_review_by_id(db: Session, id: int) -> Optional[models.Review]:
    db_review = db.scalars(
        select(tables.Review).where(tables.Review.id == id)
    ).first()
    return models.Review.model_validate(db_review) if db_review else None


def get_review_by_slug(db: Session, slug: str) -> Optional[models.Review]:
    db_review = db.scalars(
        select(tables.Review).where(tables.Review.slug == slug)
    ).first()
    return models.Review.model_validate(db_review) if db_review else None


def create_review(db: Session, review: models.ReviewCreate) -> tables.Review:
    db_review = tables.Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(
    db: Session,
    review: models.Review
) -> Optional[tables.Review]:
    db_review = db_review = db.scalars(
        select(tables.Review).where(tables.Review.id == review.id)
    ).first()
    if not db_review:
        return None
    for k, v in review.__dict__.items():
        if getattr(db_review, k) != v:
            setattr(db_review, k, v)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
