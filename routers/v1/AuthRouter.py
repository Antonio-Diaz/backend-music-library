from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from services.AuthService import AuthService

AuthRouter = APIRouter()

@AuthRouter.post("/auth/usuario")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), authService: AuthService = Depends()):
   return authService.login_for_access_token(form_data)

