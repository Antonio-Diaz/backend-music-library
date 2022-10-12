from fastapi import Depends

from models.InformationModel import Information
from models.UserModel import User
from repositories.InformationRepository import InformationRepository
from repositories.UserRepository import UserRepository
from schemas.pydantic.InformationSchema import InformationGetREquestSchema, InformationPostRequestSchema, InformationSchema, InformationPatchRequestSchema, InformationSoftDeleteRequestSchema
from services.AuthService import AuthService

class InformationService:
    informationRespository: InformationRepository
    
    def __init__(self, informationRepository: InformationRepository = Depends(), userRepository: UserRepository = Depends()) -> None:
        self.informationRepository = informationRepository
    
    def create(self, info_body: InformationPostRequestSchema):
        return self.informationRepository.create(Information(name=info_body.name, last_name=info_body.last_name, birth_date=info_body.birth_date, phone=info_body.phone, gender=info_body.gender), username=info_body.username, password=info_body.password)
    
    def get(self, user_id: int, authService: AuthService):
        return self.informationRepository.get(user_id)
    
    def update(self, info_body: InformationPatchRequestSchema) -> Information:
        return self.informationRepository.update(Information(**info_body.dict()))
    
    def delete(self, info_body: InformationSoftDeleteRequestSchema) -> Information:
        return self.informationRepository.delete(Information(**info_body.dict()))