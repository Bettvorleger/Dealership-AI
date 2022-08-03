from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.cars as crud
from src.auth.jwthandler import get_current_user
from src.schemas.cars import CarOutSchema, CarInSchema, UpdateCar
from src.schemas.token import Status
from src.schemas.users import UserOutSchema


router = APIRouter()


@router.get(
    "/cars",
    response_model=List[CarOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_cars():
    return await crud.get_cars()


@router.get(
    "/car/{car_id}",
    response_model=CarOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_car(car_id: int) -> CarOutSchema:
    try:
        return await crud.get_car(car_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Car does not exist",
        )


@router.post(
    "/cars", response_model=CarOutSchema
)
async def create_car(
    car: CarInSchema) -> CarOutSchema:
    return await crud.create_car(car)

###
### todo: @router.patch ###
###

@router.patch(
    "/car/{car_id}",
    dependencies=[Depends(get_current_user)],
    response_model=CarOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_car(
    car_id: int,
    car: UpdateCar,
    current_user: UserOutSchema = Depends(get_current_user),
) -> CarOutSchema:
    return await crud.update_car(car_id, car, current_user)

@router.delete(
    "/car/{car_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_car(
    car_id: int, current_user: UserOutSchema = Depends(get_current_user)
):
    return await crud.delete_car(car_id, current_user)