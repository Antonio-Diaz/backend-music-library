from fastapi import APIRouter, Depends

from schemas.pydantic.InformationSchema import (
    InformationPatchRequestSchema,
    InformationPostRequestSchema,
    InformationSoftDeleteRequestSchema,
)
from services.InformationService import InformationService
from utils.Auth import get_current_user
InformationRouter = APIRouter()


@InformationRouter.post("/usuarios")
def create(
    information: InformationPostRequestSchema,
    informationService: InformationService = Depends(),
):
    return informationService.create(information)


@InformationRouter.get("/usuarios/{user_id}")
def get(
    user_id: int,
    informationService: InformationService = Depends(),
    user: dict = Depends(get_current_user)
):
    return informationService.get(user_id)


@InformationRouter.patch("/usuarios")
def update(
    information: InformationPatchRequestSchema,
    informationService: InformationService = Depends(),
    user: dict = Depends(get_current_user)
):
    return informationService.update(information, user)


@InformationRouter.delete("/usuarios")
def delete(
    information: InformationSoftDeleteRequestSchema,
    informationService: InformationService = Depends(),
    user: dict = Depends(get_current_user)
):
    return informationService.delete(information, user)
