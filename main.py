from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()


# app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


reviews = [
    { "name": "Fortunato Bros", "slug": "fortunato-bros" },
    { "name": "Regina Bakery", "slug": "regina-bakery" }
]


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Cannoli Reviews",
        "reviews": reviews
    })


@app.get("/reviews/{review_slug}", response_class=HTMLResponse)
def get_review(request: Request, review_slug: str):
    valid_reviews = { r["slug"] for r in reviews }
    if review_slug not in valid_reviews:
        return HTMLResponse(status_code=404)
    
    review = [r for r in reviews if r["slug"] == review_slug][0]

    return templates.TemplateResponse("review.html", {
        "request": request,
        "title": f'Review - {review["name"]}',
        "review": review
    })
