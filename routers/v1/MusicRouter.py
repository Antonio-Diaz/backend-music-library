from fastapi import APIRouter, Depends
from models.UserModel import User

from services.MusicService import MusicService
from repositories.AuthRepository import AuthRepository
from schemas.pydantic.MusicSchema import (
    MusicPostRequestSchema,
    MusicPatchRequestSchema,
    MusicDeleteRequestSchema,
)
from utils.Auth import get_current_user

MusicRouter = APIRouter()


@MusicRouter.get("/usuarios/mimusica/")
def index(
    user: dict = Depends(get_current_user), musicService: MusicService = Depends()
):
    return musicService.index(user_id=user.get("user_id"))


@MusicRouter.post("/usuarios/mimusica")
def create(
    music: MusicPostRequestSchema,
    musicService: MusicService = Depends(),
    user: dict = Depends(get_current_user),
):
    return musicService.create(music, user)


@MusicRouter.get("/usuarios/mimusica/{user_id}")
def get(
    user_id: int,
    musicService: MusicService = Depends(),
    user: dict = Depends(get_current_user),
):
    return musicService.get(user_id)


@MusicRouter.patch("/usuarios/mimusica")
def update(
    music: MusicPatchRequestSchema,
    musicService: MusicService = Depends(),
    user: dict = Depends(get_current_user),
):
    return musicService.update(music, user)


@MusicRouter.delete("/usuarios/mimusica")
def delete(
    music: MusicDeleteRequestSchema,
    musicService: MusicService = Depends(),
    user: dict = Depends(get_current_user),
):
    return musicService.delete(music, user)
