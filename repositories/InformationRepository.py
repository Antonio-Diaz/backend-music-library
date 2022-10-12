from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import exc


from config.Database import get_db_connection

from models.InformationModel import Information
from models.UserModel import User

from utils.passwords import encrypt_password
from utils.Responses import ResponseSuccess, ResponseFailure, ResponseWarning
from repositories.AuthRepository import AuthRepository

class InformationRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def create(self, information: Information, username: str, password: str):
        try:
            if self.db.query(User).filter(User.username == username).first():
                return ResponseWarning(detail="Username already exists")

            if self.db.query(Information).filter(Information.phone == information.phone).first():
                return ResponseWarning(detail="Phone already exists")

            hash_password = encrypt_password(password)

            self.db.add(information)
            self.db.commit()
            self.db.refresh(information)

            user_model = User()
            user_model.username = username
            user_model.password = hash_password
            user_model.information_id = information.id

            self.db.add(user_model)
            self.db.commit()
            self.db.refresh(user_model)
            return ResponseSuccess(result="User created successfully")
        except exc.DatabaseError as e:
            return ResponseFailure(detail=str(e))
        
        
    def get(self, user_id: int):
        try:
            info_model = self.db.query(Information).filter(Information.id == user_id).first()
            user_model = self.db.query(User).filter(User.information_id == info_model.id).first()
            
            if user_model.is_active:
                return ResponseSuccess(result=[{
                    "user_id": user_model.id,
                    "detials": {
                        "username": user_model.username,
                        "email": user_model.email,
                        "rol": user_model.rol,
                        "telefono": info_model.phone,
                        "nombre": info_model.name,
                        "genero": info_model.gender,
                        "fecha_nacimiento": info_model.birth_date,
                    },
                }])
            
        except exc.DatabaseError as e:
            return ResponseFailure(detail=str(e))

    def update(self, information: Information):
        try:
            self.db.merge(information)
            self.db.commit()
            return ResponseSuccess(result="User updated successfully")    
        except exc.DatabaseError as e:
            return ResponseFailure(detail=str(e))


    def delete(self, information: Information):
        try:
            user = self.db.get(User, information.id)
            user.is_active = False            
            self.db.merge(user)
            self.db.commit()
            return ResponseSuccess(result="User deleted successfully")
        except exc.DatabaseError as e:
            return ResponseFailure(detail=str(e))
