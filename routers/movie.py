from fastapi import APIRouter
from fastapi import Path, Query, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from middlewares.jwt_bearer import JWTBearer
from config.database import Session
from models.movie import Movie as MovieModel
from schemas.movie import Movie
from fastapi.encoders import jsonable_encoder
from services.movie import MovieService

movie_router = APIRouter()

@movie_router.get('/movies', tags = ['Movies'], summary= "Get all movies", response_model = List[Movie], dependencies= [Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    try:
        db = Session()
    except HTTPException as e:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
    
    else:
        result = MovieService(db).get_movies()
        return JSONResponse(status_code = status.HTTP_200_OK, content = jsonable_encoder(result))

@movie_router.get(path= '/movies/{id}', tags = ["Movies"], summary= "Get one movie", response_model = Movie)
def get_movie(id: int =  Path(ge=1, le=200)) -> Movie:
    try:
        db = Session()
    except HTTPException as e:
        return HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(e))
    
    else:
        result = MovieService(db).get_movie(id)

        if not result:
            return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content= {"message": "No encontrada"})
        
        return JSONResponse(status_code= status.HTTP_200_OK, content = jsonable_encoder(result))

@movie_router.get(path= "/movies/", summary="Get movie by category", tags = ["Movies"], response_model = List[Movie], status_code= status.HTTP_200_OK)
def get_movie_by_category(category: str = Query(min_length= 5, max_length= 15)) -> List[Movie]:
    try:
        db = Session()
    except HTTPException as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
    
    else:
        result = MovieService(db).get_movies_by_category(category)

        if not result:
            return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content = {"Error": "Movies in that category not found!"})
        
        return JSONResponse(status_code =  status.HTTP_200_OK, content = jsonable_encoder(result))
            
@movie_router.post(path = "/movies", tags = ["Movies"], summary= "Add a new movie to films", response_model= dict, status_code=status.HTTP_201_CREATED)
async def register_movie(new_movie: Movie) -> dict:
    try:
        db = Session()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(e))
    
    else:
        MovieService(db).create_movie(new_movie)
        return JSONResponse(content = {"message":"Movie sucessfully registered!"}, status_code= status.HTTP_201_CREATED)

@movie_router.put(path = "/movies/{id}", tags = ["Movies"], summary = "Update movie", response_model = dict, status_code= status.HTTP_200_OK)
def update_movie(id: int, film: Movie) -> dict:
    try:
        db = Session()
    except HTTPException as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= str(e))
    
    else:
        movie_update = MovieService(db).get_movie(id)

        if not movie_update:
            return JSONResponse(status_code= status.HTTP_404_NOT_FOUND, content= {"message":"ID not found"})
        
        MovieService(db).update_movie(id, film)
        return JSONResponse(content = {"message":"Movie successfully updated!", "details": jsonable_encoder(movie_update)})
        
@movie_router.delete(path = "/movies/{id}", tags = ["Movies"], summary= "Delete a movie", response_model = dict, status_code= status.HTTP_200_OK)
def delete_movie(id: int) -> dict:
    try:
        db = Session()
    except HTTPException as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
    
    else:
        result = MovieModel(db).get_movie(id)

        if not result:
            return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content =  {"message": "ID not found"})
        
        db.delete(result)
        db.commit()
        return JSONResponse(status_code= status.HTTP_200_OK, content = "Record deleted")
    
