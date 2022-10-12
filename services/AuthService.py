from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from repositories.AuthRepository import AuthRepository

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

class AuthService:
        authRepository: AuthRepository
        
        def __init__(self, authRepository: AuthRepository = Depends()) -> None:
            self.authRepository = authRepository
            
        def login_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
            return self.authRepository.login_for_access_token(form_data)
        