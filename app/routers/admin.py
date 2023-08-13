import datetime
from typing import Annotated

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models import Review


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def admin_home(request: Request):
    return templates.TemplateResponse("admin.html", { "request": request })


@router.post("/review")
async def create_review(
    request: Request,
    title: Annotated[str, Form()],
    location: Annotated[str, Form()],
    date: Annotated[datetime.date, Form()],
    slug: Annotated[str, Form()],
    summary: Annotated[str, Form()],
    liked: Annotated[str, Form()],
    disliked: Annotated[str, Form()],
    rating: Annotated[float, Form()],
    tags: Annotated[str, Form()]
):
    review = Review(
        title=title,
        location=location,
        date=date,
        slug=slug,
        summary=summary,
        liked=liked,
        disliked=disliked,
        rating=rating,
        tags=tags.replace(" ", "").split(",")
    )
    print(review)
    return { "review": review.model_dump() }
