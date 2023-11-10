from pydantic import BaseModel, Field
from typing import Optional

# Esquema
class Movie(BaseModel):
    id: Optional[int] = None
    overview: str
    title: str = Field(min_length= 5, max_length= 15)
    year: int = Field(le= 2023)
    director: str = Field(min_length= 3)
    category: str
    rating: float
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                "id": 1,
                "overview": "Resumen",
                "title": "Nombre de la peli",
                "director": "Quien la dirige",
                "year": 2023,
                "category": "Género de peli",
                "rating": 9.0
            }
            ]
        }
   }