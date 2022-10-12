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


@router.post("/usuarios", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserModel, db: Session = Depends(get_db)):
    try:
        # Check if phone and username already takens
        phoneFound = check_if_exists_field(
            db, Information, Information.phone, user.phone
        )
        if phoneFound:
            return Response.__repr__(
                Response(is_error=True, details="Phone already exists")
            )

        usernameFound = check_if_exists_field(db, User, User.username, user.username)
        if usernameFound:
            return Response.__repr__(
                Response(is_error=True, details="Username already exists")
            )

        information_model = Information()
        information_model.name = user.name
        information_model.last_name = user.last_name
        information_model.birth_date = user.birth_date
        information_model.phone = user.phone
        information_model.gender = user.gender

        db.add(information_model)
        db.commit()
        db.refresh(information_model)

        user_model = User()
        user_model.username = user.username
        hash_password = encrypt_password(user.password)
        user_model.password = hash_password
        user_model.information_id = information_model.id

        db.add(user_model)
        db.commit()
        db.refresh(user_model)

        return Response.__repr__(
            Response(is_error=False, result="User created successfully")
        )
    except exc.DatabaseError as e:
        return Response.__repr__(
            Response(is_error=True, details="Something went wrong")
        )


@router.get("/usuarios/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return Response.__repr__(Response(is_error=True, details="User not found"))
        return user
    except exc.DatabaseError as e:
        return Response.__repr__(
            Response(is_error=True, details="Something went wrong")
        )


@router.delete("/usuarios")
async def delete_user_by_id(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    try:
        if user is None:
            db.query(User).update({User.is_active: False}).where(
                User.id == user.get("user_id")
            )
            db.commit()
            db.refresh(user)
            return Response.__repr__(
                Response(is_error=False, result="User deleted successfully")
            )
        return Response.__repr__(Response(is_error=True, details="User not found"))
    except exc.DatabaseError as e:
        return Response.__repr__(
            Response(is_error=True, details="Something went wrong")
        )

