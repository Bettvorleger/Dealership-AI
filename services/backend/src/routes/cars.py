from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.cars as crud
from src.auth.jwthandler import get_current_user
from src.schemas.cars import CarOutSchema, CarOutTrainSchema, Filter, CarInSchema, UpdateCar, InferenceCar
from src.schemas.token import Status


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


@router.patch(
    "/car/{car_id}",
    dependencies=[Depends(get_current_user)],
    response_model=CarOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_car(
    car_id: int,
    car: UpdateCar,
) -> CarOutSchema:
    return await crud.update_car(car_id, car)


@router.delete(
    "/car/{car_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_car(
    car_id: int
):
    return await crud.delete_car(car_id)


@router.get(
    "/filter",
    response_model=Filter
)
async def get_filters() -> Filter:
    return await crud.get_filter()


@router.post(
    "/price",
    response_model=int
)
async def get_price(car: InferenceCar) -> int:
    return await crud.get_price(car)


@router.get(
    "/soldCars",
    response_model=List[CarOutTrainSchema],
)
async def get_sold_cars():
    return await crud.get_sold_cars()