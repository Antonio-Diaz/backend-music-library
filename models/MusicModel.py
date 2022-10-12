from sqlalchemy import Column, Integer, String, ForeignKey
from models.BaseModel import EntityMeta


class Music(EntityMeta):
    __tablename__ = "music"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    author = Column(String(50))

    information_id = Column(Integer, ForeignKey("information.id"))
