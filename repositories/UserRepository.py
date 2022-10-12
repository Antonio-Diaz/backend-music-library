from fastapi import Depends
from sqlalchemy.orm import Session

from config.Database import get_db_connection

from models.InformationModel import Information
from models.UserModel import User


class UserRepository:
    db: Session
    
    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db
        
    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get(self, id: int) -> User:
        return self.db.get(User, id)
    
    def update(self, id: int, user: User) -> User:
        user.id = id
        self.db.merge(user)
        self.db.commit()
        return user
    
    def delete(self, id: int) -> None:
        self.db.delete(self.get(id))
        self.db.commit()
        self.db.flush()