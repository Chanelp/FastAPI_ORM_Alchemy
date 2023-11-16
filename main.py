from fastapi import FastAPI
from utils.jwt_manager import create_token
from config.database import Base, engine
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import login_router

app = FastAPI()
app.title = "First Application Programming Interface with FastApi"
app.version = "0.0.2"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(login_router)

Base.metadata.create_all(bind = engine)
