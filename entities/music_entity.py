from optparse import Option
from typing import Optional
from unicodedata import name
from pydantic import BaseModel, validator


class MusicModel(BaseModel):
    name: str
    author: str

    @validator("name")
    def name_must_be_string(cls, v):
        if not isinstance(v, str):
            raise ValueError("Name must be a string")
        return v.title()

    @validator("author")
    def author_must_be_string(cls, v):
        if not isinstance(v, str):
            raise ValueError("Author must be a string")
        return v.title()


class UpdateMusicModel(BaseModel):
    id: int
    name: Optional[str] 
    author: Optional[str]