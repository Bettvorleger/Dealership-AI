from tortoise import fields, models


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    full_name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class Cars(models.Model):
    id = fields.IntField(pk=True)
    # features
    make = fields.CharField(max_length=225)
    model = fields.CharField(max_length=225)
    mileage = fields.IntField()
    fuel = fields.CharField(max_length=50)
    gear = fields.CharField(max_length=50)
    offer_type = fields.CharField(max_length=50)
    hp = fields.IntField()
    year = fields.IntField()
    price = fields.IntField()
    # for sales prediction
    is_custom = fields.BooleanField()
    is_sold = fields.BooleanField()

    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
