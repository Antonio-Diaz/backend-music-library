from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import exc
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from config.Database import get_db_connection

from models.UserModel import User
from schemas.pydantic.AuthSchema import AuthLoginSchema
from utils.CustomException import get_token_exception, get_user_exception

from utils.Responses import ResponseSuccess, ResponseFailure, ResponseWarning
from utils.fields import check_if_exists_field
from utils.passwords import check_encrypted_password
from config.Environment import get_environment_variable

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
env = get_environment_variable()

class AuthRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def authenticate_user(self, data: AuthLoginSchema):
        user = check_if_exists_field(self.db, User, User.username, data.username)
        if not user:
            return False
        if not check_encrypted_password(data.password, user.password):
            return False
        return user

    def create_access_token(
        self, username: str, user_id: int, expires_delta: Optional[timedelta] = None
    ):
        to_encode = {"username": username, "user_id": user_id}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm=env.ALGORITHM)
        return encoded_jwt

    def get_current_user(self, token: str = Depends(oauth2_schema)):
        try:
            payload = jwt.decode(token, env.SECRET_KEY, algorithms=[env.ALGORITHM])
            username: str = payload.get("username")
            user_id: int = payload.get("user_id")
            if username is None or user_id is None:
                raise get_user_exception()
            return {"username": username, "user_id": user_id}
        except JWTError:
            return get_user_exception()

    def login_for_access_token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        try:
            user = self.authenticate_user(form_data)
            if not user:
                return get_token_exception()
            return {
                "access_token": self.create_access_token(user.username, user.id),
                "token_type": "bearer",
            }
        except exc.DatabaseError as e:
            return ResponseFailure(detail=str(e))
