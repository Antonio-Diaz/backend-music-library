from turtle import clear
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Boolean

import enum
from datetime import datetime
from sqlalchemy.sql import func
from models.BaseModel import EntityMeta

class RolType(enum.Enum):
    admin = 1
    user = 2
    guest = 3


class User(EntityMeta):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    rol = Column(Enum(RolType), default=RolType.user)
    email = Column(String(50), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(60))
    is_active = Column(Boolean, default=True)
    token = Column(String(60), default="")
    token_recovery = Column(String(60), default="")
    created_at = Column(DateTime(timezone=True), default=datetime.now())
    updated_at = Column(
        DateTime(timezone=True), default=datetime.now(), onupdate=func.now()
    )
    deleted_at = Column(DateTime(timezone=True), default=None)

    information_id = Column(Integer, ForeignKey("information.id"))