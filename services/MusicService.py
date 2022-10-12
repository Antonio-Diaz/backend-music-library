from fastapi import Depends

from models.MusicModel import Music
from repositories.MusicRepository import MusicRepository
from schemas.pydantic.MusicSchema import ( MusicPostRequestSchema, MusicPatchRequestSchema, MusicDeleteRequestSchema, MusicSchema )

class MusicService:
    musicRespository: MusicRepository
    
    def __init__(self, musicRespository: MusicRepository = Depends()) -> None:
        self.musicRespository = musicRespository
    
    def index(self, user_id: int):
        return self.musicRespository.index(user_id=user_id)
    
    def create(self, music_body: MusicPostRequestSchema, user: dict):
        return self.musicRespository.create(Music(name=music_body.name, author=music_body.author, information_id=user.get("user_id")))
    
    def get(self, user_id: int):
        return self.musicRespository.get(user_id)
    
    def update(self, music_body: MusicPatchRequestSchema, user: dict):
        return self.musicRespository.update(Music(id=music_body.id, name=music_body.name, author=music_body.author, information_id=user.get("user_id")))
    
    def delete(self, music_body: MusicDeleteRequestSchema, user: dict):
        return self.musicRespository.delete(music_body.id, user_id=user.get("user_id"))