from unittest import result
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import exc


from config.Database import get_db_connection

from models.MusicModel import Music

from utils.Responses import ResponseSuccess, ResponseFailure, ResponseWarning


class MusicRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def index(self, user_id: int):
        try:
            musics = self.db.query(Music).filter(Music.information_id == user_id).all()
            if musics:
                return ResponseSuccess(result=list(musics))
            return ResponseSuccess(result=list())
        except exc.DatabaseError as e:
            return ResponseFailure(detail=str(e))

    def create(self, music: Music):
        try:
            self.db.add(music)
            self.db.commit()
            self.db.refresh(music)
            return ResponseSuccess(result=music)
        except exc.DatabaseError as e:
            return ResponseFailure(detail=str(e))

    def get(self, user_id: int):
        try:
            music = self.db.query(Music).filter(Music.information_id == user_id).first()
            if music:
                return ResponseSuccess(result=music)
            return ResponseWarning(detail="Music not found")
        except exc.DatabaseError as e:
            return ResponseFailure(detail=str(e))

    def update(self, music: Music):
        try:
            self.db.merge(music)
            self.db.commit()
            self.db.refresh(music)
            return ResponseSuccess(result="Music updated successfully")
        except exc.DatabaseError as e:
            return ResponseFailure(detail=str(e))

    def delete(self, music_id: int, user_id: int):
        try:
            music = (
                self.db.query(Music)
                .filter(Music.id == music_id, Music.information_id == user_id)
                .first()
            )
            if music:
                self.db.delete(music)
                self.db.commit()
                return ResponseSuccess(result="Music deleted successfully")
            return ResponseWarning(detail="Music not found")
        except exc.DatabaseError as e:
            return ResponseFailure(detail=str(e))
