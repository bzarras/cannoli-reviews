from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db import get_all_reviews


router = APIRouter()


templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    reviews = [r.model_dump() for r in get_all_reviews()]
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Cannoli Reviews",
        "reviews": reviews
    })


@router.get("/reviews/{review_slug}", response_class=HTMLResponse)
async def get_review(request: Request, review_slug: str):
    reviews = get_all_reviews()
    valid_reviews = { r.slug for r in reviews }
    if review_slug not in valid_reviews:
        return HTMLResponse(status_code=404)
    
    review = [r for r in reviews if r.slug == review_slug][0]

    return templates.TemplateResponse("review.html", {
        "request": request,
        "title": f'Review - {review.title}',
        "review": review.model_dump()
    })
