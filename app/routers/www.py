from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.managers import images, reviews


router = APIRouter()


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, order_by: Optional[str] = None, db: Session = Depends(get_db)):
    db_reviews = [r.model_dump() for r in reviews.get_reviews(db, order_by)]
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Cannoli Reviews",
        "reviews": db_reviews
    })


@router.get("/reviews/{review_slug}", response_class=HTMLResponse)
async def get_review(request: Request, review_slug: str, db: Session = Depends(get_db)):
    review = reviews.get_review_by_slug(db, review_slug)

    if not review:
        return HTMLResponse(status_code=404)

    return templates.TemplateResponse("review.html", {
        "request": request,
        "title": f'Review - {review.title}',
        "review": review.model_dump()
    })


@router.get("/img/{img_name}", response_class=Response)
async def get_image(img_name: str, db: Session = Depends(get_db)):
    image = images.get_image_by_name(db, img_name)
    
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return Response(content=image.data, media_type=f"image/{image.type}")
