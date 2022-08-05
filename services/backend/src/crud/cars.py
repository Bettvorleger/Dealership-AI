from fastapi import HTTPException
from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist
import json

import src.inference as inference
from src.database.models import Cars
from src.schemas.cars import CarOutSchema, CarOutTrainSchema, Filter
from src.schemas.token import Status


async def get_cars():
    return await CarOutSchema.from_queryset(Cars.all())


async def get_car(car_id) -> CarOutSchema:
    return await CarOutSchema.from_queryset_single(Cars.get(id=car_id))


async def get_filter() -> Filter:
    filter = json.loads(open("src/assets/filter.json", "r").read())
    return filter


async def create_car(car) -> CarOutSchema:
    car_dict = car.dict(exclude_unset=True)
    car_dict["is_sold"] = False
    car_obj = await Cars.create(**car_dict)
    return await CarOutSchema.from_tortoise_orm(car_obj)


async def update_car(car_id, car) -> CarOutSchema:
    try:
        await CarOutSchema.from_queryset_single(Cars.get(id=car_id))
    except DoesNotExist:
        raise HTTPException(
            status_code=404, detail=f"Car {car_id} not found")

    await Cars.filter(id=car_id).update(**car.dict(exclude_unset=True))
    return await CarOutSchema.from_queryset_single(Cars.get(id=car_id))


async def delete_car(car_id) -> Status:
    deleted_count = await Cars.filter(id=car_id).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=404, detail=f"Car {car_id} not found")
    return Status(message=f"Deleted car {car_id}")


async def get_price(car) -> int:
    price = await inference.predict(car)
    return price


async def get_sold_cars():
    return await CarOutTrainSchema.from_queryset(Cars.filter(is_sold='true'))
