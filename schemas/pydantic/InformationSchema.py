from pydantic import BaseModel
from typing import Optional
    
class InformationPostRequestSchema(BaseModel):
    name: str
    last_name: str
    birth_date: str
    phone: str
    gender: str
    username: str
    password: str

class InformationPatchRequestSchema(BaseModel):
    name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[str]

class InformationSoftDeleteRequestSchema(BaseModel):
    id: int

class InformationGetREquestSchema(BaseModel):
    id: int

class InformationSchema(InformationPostRequestSchema):
    pass