from typing import List, Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Cars


CarInSchema = pydantic_model_creator(
    Cars, name="CarsIn", exclude=["is_sold"], exclude_readonly=True)

CarOutSchema = pydantic_model_creator(
    Cars, name="Car", exclude=["modified_at"])


# just for filter
class Filter(BaseModel):
    make: Optional[List]
    model: Optional[dict]
    fuel: Optional[List]


# just for patch
class UpdateCar(BaseModel):
    make: Optional[str]
    model: Optional[str]
    mileage: Optional[int]
    fuel: Optional[str]
    gear: Optional[str]
    offer_type: Optional[str]
    hp: Optional[int]
    year: Optional[int]
    price: Optional[int]
    is_sold: Optional[bool]


# just for patch
class InferenceCar(BaseModel):
    make: Optional[str]
    model: Optional[str]
    mileage: Optional[int]
    fuel: Optional[str]
    gear: Optional[str]
    offer_type: Optional[str]
    hp: Optional[int]
    year: Optional[int]
