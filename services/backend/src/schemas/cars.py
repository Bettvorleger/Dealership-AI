from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Cars


CarInSchema = pydantic_model_creator(
    Cars, name="CarsIn", exclude=["author_id", "is_sold", "price"], exclude_readonly=True)

CarOutSchema = pydantic_model_creator(
    Cars, name="Car", exclude =["modified_at", "author.password", "author.created_at", "author.modified_at"])

#just for patch
'''
class UpdateCar(BaseModel):
    title: Optional[str]
    make = Optional[str]
    model = Optional[str]
    mileage = Optional[int]
    fuel = Optional[str]
    gear = Optional[str]
    offer_type = Optional[str]
    hp = Optional[int]
    year = Optional[int]
    price = Optional[int]'''