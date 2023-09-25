import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.managers import images, reviews
from app.models import ReviewCreate, ImageCreate


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def admin_home(request: Request, db: Session = Depends(get_db)):
    image_names = images.get_image_names(db)
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "img_urls": [f"/img/{n}" for n in image_names]
    })


# TODO: need a way to protect against anyone being able to upload images
@router.post("/images", response_class=RedirectResponse)
async def create_image(file: UploadFile, db: Session = Depends(get_db)):
    print(f"Uploading image {file.filename}")

    file_contents = await file.read()

    image = ImageCreate(
        name=file.filename,
        data=file_contents
    )

    images.create_image(db=db, image=image)

    return RedirectResponse(url="/admin/", status_code=302)  # 302 is necessary to use GET


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

    return RedirectResponse(url="/admin/", status_code=302)
