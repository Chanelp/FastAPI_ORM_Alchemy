from jwt_manager import validate_token
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException

# Función para pasar token a las peticiones
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            return HTTPException(status_code= 403, detail= "Credentials are not valid!")