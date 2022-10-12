import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from models.BaseModel import EntityMeta


class GenderType(enum.Enum):
    M = "M"
    F = "F"
    O = "O"


class Information(EntityMeta):
    __tablename__ = "information"
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(10), unique=True, index=True)
    name = Column(String(50))
    last_name = Column(String(50))
    birth_date = Column(String(10))
    gender = Column(Enum(GenderType))

    user = relationship("User", uselist=False, backref="information")
    music = relationship("Music", backref="information")

    
