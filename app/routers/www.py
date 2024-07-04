from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.managers import (
  images as images_manager,
  reviews as reviews_manager,
)


def _should_autoescape_html(template_name: str) -> bool:
    if template_name == "map.html":
        return False
    return True


router = APIRouter()

templates = Jinja2Templates(directory="templates", autoescape=_should_autoescape_html)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, order_by: Optional[str] = None, db: Session = Depends(get_db)):
    db_reviews = [r.model_dump() for r in reviews_manager.get_reviews(db, order_by)]
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Cannoli Reviews",
        "reviews": db_reviews
    })


@router.get("/map", response_class=HTMLResponse)
async def map_view(request: Request, db: Session = Depends(get_db)):
    db_reviews_json = [r.model_dump_json() for r in reviews_manager.get_reviews(db)]
    return templates.TemplateResponse("map.html", {
        "request": request,
        "title": "Cannoli Reviews - Map",
        "reviews_json": db_reviews_json
    })


@router.get("/reviews.json", response_class=JSONResponse)
async def get_reviews_json(request: Request, db: Session = Depends(get_db)):
    db_reviews = [r.model_dump() for r in reviews_manager.get_reviews(db)]
    return db_reviews


@router.get("/reviews/{review_slug}", response_class=HTMLResponse)
async def get_review(request: Request, review_slug: str, db: Session = Depends(get_db)):
    review = reviews_manager.get_review_by_slug(db, review_slug)

    if not review:
        return HTMLResponse(status_code=404)

    return templates.TemplateResponse("review.html", {
        "request": request,
        "title": f'Review - {review.title}',
        "review": review.model_dump()
    })


@router.get("/img/{img_name}", response_class=Response)
async def get_image(img_name: str, db: Session = Depends(get_db)):
    image = images_manager.get_image_by_name(db, img_name)
    
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    headers = {}
    # these headers help with browser caching
    if image.etag:
        headers["Etag"] = image.etag
    if image.updated_at:
        headers["Last-Modified"] = image.updated_at.strftime('%a, %d %b %Y %H:%M:%S GMT')

    return Response(
        content=image.data,
        headers=headers,
        media_type=f"image/{image.type}",
    )
