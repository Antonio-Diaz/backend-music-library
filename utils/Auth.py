from fastapi import Depends
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

from utils.CustomException import get_user_exception
from config.Environment import get_environment_variables

env = get_environment_variables()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_schema)):
        try:
            payload = jwt.decode(token, env.SECRET_KEY, algorithms=[env.ALGORITHM])
            username: str = payload.get("username")
            user_id: int = payload.get("user_id")
            if username is None or user_id is None:
                raise get_user_exception()  
            return {"username": username, "user_id": user_id}
        except JWTError:
            return get_user_exception()