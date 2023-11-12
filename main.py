from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from jwt_manager import create_token
from config.database import Base, engine
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router

app = FastAPI()
app.title = "First Application Programming Interface with FastApi"
app.version = "0.0.2"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)

Base.metadata.create_all(bind = engine)
