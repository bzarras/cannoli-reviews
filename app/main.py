from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import www, admin


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(www.router)
app.include_router(admin.router, prefix="/admin")
