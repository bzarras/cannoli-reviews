from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import www


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(www.router)
