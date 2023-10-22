import datetime
import hashlib
import os
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, Request, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.managers import images, reviews
from app.models import ReviewUpdate, ReviewCreate, ImageCreate

router = APIRouter()

templates = Jinja2Templates(directory="templates")


def get_token(token: Optional[str] = None) -> str:
    if token != os.getenv("ADMIN_TOKEN"):
        raise HTTPException(status_code=403)
    return token


@router.get("/", response_class=HTMLResponse)
async def admin_home(
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    image_names = images.get_image_names(db)
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "img_urls": [f"/img/{n}" for n in image_names],
        "token": token,
    })


@router.post("/images", response_class=RedirectResponse)
async def create_image(
    file: UploadFile,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    if file.size > 10000000: # 10 MB limit, to avoid DDOS from hashing
        raise HTTPException(status_code=400, detail="File cannot be larger than 10 MB")

    file_contents = await file.read()
    etag = hashlib.md5(file_contents).hexdigest()

    image = ImageCreate(
        name=file.filename,
        data=file_contents,
        etag=etag,
    )

    images.create_image(db=db, image=image)

    return RedirectResponse(url=f"/admin?token={token}", status_code=302)  # 302 is necessary to use GET


@router.post("/reviews")
async def create_review(
    title: Annotated[str, Form()],
    location: Annotated[str, Form()],
    date: Annotated[datetime.date, Form()],
    slug: Annotated[str, Form()],
    summary: Annotated[str, Form()],
    liked: Annotated[str, Form()],
    disliked: Annotated[str, Form()],
    rating: Annotated[float, Form()],
    img_url: Annotated[str, Form()],
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    review = ReviewCreate(
        title=title,
        location=location,
        date=date,
        slug=slug,
        summary=summary,
        liked=liked,
        disliked=disliked,
        rating=rating,
        img_url=img_url
    )

    reviews.create_review(db=db, review=review)

    return RedirectResponse(url=f"/admin?token={token}", status_code=302)


@router.get("/reviews")
async def get_reviews(
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    db_reviews = reviews.get_reviews(db=db, _all=True)
    return templates.TemplateResponse("admin_reviews.html", {
        "request": request,
        "reviews": db_reviews,
        "token": token,
    })


@router.get("/reviews/{review_id}")
async def get_review(
    request: Request,
    review_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    review = reviews.get_review_by_id(db=db, id=review_id)
    image_names = images.get_image_names(db)
    if not review:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("admin_edit_review.html", {
        "request": request,
        "review": review,
        "img_urls": [f"/img/{n}" for n in image_names],
        "token": token
    })


@router.post("/reviews/{review_id}")
async def update_review(
    review_id: int,
    title: Annotated[str, Form()],
    location: Annotated[str, Form()],
    date: Annotated[datetime.date, Form()],
    slug: Annotated[str, Form()],
    summary: Annotated[str, Form()],
    liked: Annotated[str, Form()],
    disliked: Annotated[str, Form()],
    rating: Annotated[float, Form()],
    img_url: Annotated[str, Form()],
    link: Annotated[str, Form()],
    visible: Annotated[bool, Form()] = False,
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    review_update = ReviewUpdate(
        id=review_id,
        title=title,
        location=location,
        date=date,
        slug=slug,
        summary=summary,
        liked=liked,
        disliked=disliked,
        rating=rating,
        img_url=img_url,
        visible=visible,
        link=link,
    )
    reviews.update_review(db=db, review_update=review_update)
    return RedirectResponse(url=f"/admin?token={token}", status_code=302)
