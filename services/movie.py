from models.movie import Movie as MovieModel
from schemas.movie import Movie

class MovieService:
    def __init__(self, db) -> None:
        self.db = db
    
    def get_movies(self):
        movies_searched = self.db.query(MovieModel).all()
        return movies_searched

    def get_movie(self, id):
        movie_searched = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return movie_searched

    def get_movies_by_category(self, category):
        movie_searched = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return movie_searched
    
    def create_movie(self, new_movie):
        movie_to_create = MovieModel(**new_movie.model_dump())
        self.db.add(movie_to_create)
        self.db.commit()
        return
    
    def update_movie(self, id: int, film: Movie):
        movie_to_update = self.get_movie(id)

        movie_to_update.title = film.title
        movie_to_update.category = film.category
        movie_to_update.director = film.director
        movie_to_update.overview = film.overview
        movie_to_update.rating = film.rating
        movie_to_update.year = film.year

        self.db.add(movie_to_update)
        self.db.commit()
        self.db.refresh(movie_to_update)

