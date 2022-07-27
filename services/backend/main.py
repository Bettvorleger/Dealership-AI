from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

# enable schemas to read relationship between models
Tortoise.init_models(["src.database.models"], "models")

# must be AFTER tortoise model init, otherwise foregin keys aren't loadded
from src.routes import users, notes, cars

subpath = '/fastapi'
app = FastAPI(docs_url=f'{subpath}/docs', openapi_url=f'{subpath}/openapi.json')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router, prefix=subpath)
app.include_router(notes.router, prefix=subpath)
app.include_router(cars.router, prefix=subpath)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


@app.get(f'{subpath}/')
def home():
    return "Hello, World 2!"
