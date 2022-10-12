from pydantic import BaseModel
from typing import Optional

class AuthLoginSchema(BaseModel):
    username: str
    password: str
    
class AuthTokenSchema(BaseModel):
    access_token: str
    token_type: str
    
class AuthTokenDataSchema(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    time_expire: Optional[int] = None