# Importar el modulo
from fastapi import FastAPI, Body, Path, Query, status, Depends
from fastapi.responses import JSONResponse
from typing import List

from jwt_manager import create_token, JWTBearer

from config.database import Session, Base, engine
from models.movie import Movie as MovieModel
from schemas.user import User

from schemas.movie import Movie

app = FastAPI()

app.title = "First Application Programming Interface with FastApi"
app.version = "0.0.2"

Base.metadata.create_all(bind = engine)

movies = [
        {
            "id": 1,
            "overview": "Lorem ipsum",
            "title": "The Galactic Adventure",
            "year": 2020,
            "category": "Sci-Fi",
            "director": "John Director",
            "rating": 8.0
        },
        {
            "id": 2,
            "overview": "Lorem ipsum",
            "title": "La Gran Comedia",
            "year": 2019,
            "category": "Comedy",
            "director": "Maria Director",
            "rating": 7.5
        },
        {
            "id": 3,
            "overview": "Lorem ipsum",
            "title": "Drama in the City",
            "year": 2021,
            "category": "Drama",
            "director": "Michael Director",
            "rating": 8.5
        },
        {
            "id": 4,
            "overview": "Lorem ipsum",
            "title": "Mystery Island",
            "year": 2018,
            "category": "Mystery",
            "director": "Emma Director",
            "rating": 9.0
        },
        {
            "id": 5,
            "overview": "Lorem ipsum",
            "title": "Aventura Extrema",
            "year": 2022,
            "category": "Adventure",
            "director": "Daniel Director",
            "rating": 7.8
        }
    ]


@app.get('/', tags = ['Home'])
def message():
    return "Learning about fastApi"

@app.get('/movies', tags = ['Movies'], summary= "Get all movies", response_model = List[Movie], dependencies= [Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(content = movies)

@app.get(path= '/movies/{id}', tags = ["Movies"], summary= "Get one movie", response_model = Movie)
def get_movie(id: int =  Path(ge=1, le=200)) -> Movie:
    try:
        movie_found = [movie for movie in movies if movie['id'] == id][0]
        return JSONResponse(content= movie_found)
    except IndexError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content= [])
    
@app.get(path= "/movies/", summary="Get movie by category", tags = ["Movies"], response_model = List[Movie], status_code= status.HTTP_200_OK)
def get_movie_by_category(category: str = Query(min_length= 5, max_length= 15)) -> List[Movie]:
    try:
        data = [ movies for movies in movies if movies['category'] == category ]
        return JSONResponse(content= data, status_code= status.HTTP_200_OK)
    except IndexError:
        return {"Error": "Movies in that category not found!"}
    
@app.post(path = "/movies", tags = ["Movies"], summary= "Add a new movie to films", response_model= dict, status_code=status.HTTP_201_CREATED)
def register_movie(new_movie: Movie) -> dict:
    db = Session()
    movie = MovieModel(**new_movie.model_dump())
    db.add(movie)
    db.commit()
    return JSONResponse(content = {"message":"Movie sucessfully registered!"}, status_code= status.HTTP_201_CREATED)

# Login
@app.post(path= "/login", tags = ["Auth"], summary= "Log In")
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.model_dump())
        return JSONResponse(status_code= status.HTTP_200_OK, content= token)
    else:
        return JSONResponse(status_code= status.HTTP_401_UNAUTHORIZED, content= {"message":"Credenciales inválidas, intente de nuevo"})

@app.put(path = "/movies/{id}", tags = ["Movies"], summary = "Update movie", response_model = dict, status_code= status.HTTP_200_OK)
def update_movie(id: int, film: Movie) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = film.title
            movie['overview'] = film.overview
            movie['year'] =  film.year
            movie['category'] = film.category
            movie['director'] = film.director
            movie['rating'] =  film.rating
            return JSONResponse(content = {"message":"Movie successfully updated!"})
        
@app.delete(path = "/movies/{id}", tags = ["Movies"], summary= "Delete a movie", response_model = dict, status_code= status.HTTP_200_OK)
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
            return JSONResponse(content= {"message":"Movie successfully removed!"}, status_code= status.HTTP_200_OK)