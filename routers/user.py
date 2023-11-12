from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from schemas.user import User
from jwt_manager import create_token

login_router = APIRouter()

@login_router.post(path= "/login", tags = ["Auth"], summary= "Log In")
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.model_dump())
        return JSONResponse(status_code= status.HTTP_200_OK, content= token)
    else:
        return JSONResponse(status_code= status.HTTP_401_UNAUTHORIZED, content= {"message":"Credenciales inválidas, intente de nuevo"})
