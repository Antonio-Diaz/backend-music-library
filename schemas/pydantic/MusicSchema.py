from pydantic import BaseModel
from typing import Optional, List


class MusicSchema(BaseModel):
    id: int
    name: str
    author: str
    information_id: int

class MusicPostRequestSchema(BaseModel):
    name: str
    author: str
    
class MusicPatchRequestSchema(BaseModel):
    id: int
    name: Optional[str]
    author: Optional[str]
    
class MusicDeleteRequestSchema(BaseModel):
    id: int
    
