import sys 
sys.path.append('..')

from http.client import HTTPException
from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import exc
from datetime import datetime

from config.Database import engine, Base

# Enttities
from entities.user_entity import UserModel
from entities.music_entity import MusicModel, UpdateMusicModel

# Models
from models.UserModel import User
from models.InformationModel import Information
from models.MusicModel import Music

# Services
from services.AuthService import get_current_user, get_user_exception

# Uitls
from utils.Responses import Response
from utils.passwords import encrypt_password
from utils.fields import check_if_exists_field
from utils.database import get_db


models = [User, Information, Music]
Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.post("/usuarios/mimusica", status_code=status.HTTP_201_CREATED)
async def create_music(
    music: MusicModel,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        if user is None:
            raise get_user_exception()
        music_model = Music()
        music_model.name = music.name
        music_model.author = music.author
        music_model.information_id = user.get("user_id")

        db.add(music_model)
        db.commit()
        db.refresh(music_model)
        return Response.__repr__(
            Response(is_error=False, result="Music created successfully")
        )
    except exc.DatabaseError as e:
        return Response.__repr__(
            Response(is_error=True, details="Something went wrong")
        )


@router.get("/usuarios/mimusica/")
async def get_musics(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    try:
        if user is None:
            raise get_user_exception()
        musics = (
            db.query(Music.id, Music.name, Music.author)
            .filter(Music.information_id == user.get("user_id"))
            .all()
        )
        return Response.__repr__(Response(is_error=False, result=musics))
    except exc.DatabaseError as e:
        return Response.__repr__(
            Response(is_error=True, details="Something went wrong")
        )


@router.get("/usuarios/mimusica/{music_id}")
async def get_music_by_id(
    music_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    try:
        if user is None:
            raise get_user_exception()
        music = db.query(Music).filter(Music.id == music_id).first()
        return Response.__repr__(Response(is_error=False, result=music))
    except exc.DatabaseError as e:
        return Response.__repr__(
            Response(is_error=True, details="Something went wrong")
        )


@router.patch("/usuarios/mimusica")
async def update_music_by_id(
    updateMusicModel: UpdateMusicModel,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        if user is None:
            raise get_user_exception()
        music = db.query(Music).filter(Music.id == updateMusicModel.id).first()
        if UpdateMusicModel.name is not None:
            music.name = UpdateMusicModel.name
        if UpdateMusicModel.author is not None:
            music.author = UpdateMusicModel.author
        db.commit()
        db.refresh(music)
        return Response.__repr__(
            Response(is_error=False, result="Music updated successfully")
        )
    except exc.DatabaseError as e:
        return Response.__repr__(
            Response(is_error=True, details="Something went wrong")
        )


@router.delete("/usuarios/mimusica/{music_id}")
async def delete_music_by_id(
    music_id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        if user is None:
            raise get_user_exception()
        music = db.query(Music).filter(Music.id == music_id).first()
        db.delete(music)
        db.commit()
        return Response.__repr__(
            Response(is_error=False, result="Music deleted successfully")
        )
    except exc.DatabaseError as e:
        return Response.__repr__(
            Response(is_error=True, details="Something went wrong")
        )
