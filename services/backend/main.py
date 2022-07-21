from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

# enable schemas to read relationship between models
Tortoise.init_models(["src.database.models"], "models")

# must be AFTER tortoise model init, otherwise foregin keys aren't loadded
from src.routes import users, notes

subpath = '/fastapi'
app = FastAPI(root_path=subpath, docs_url=f'{subpath}/docs')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router, prefix=subpath)
app.include_router(notes.router, prefix=subpath)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


@app.get(f'{subpath}/')
def home():
    return "Hello, World! TEST"

@app.get(f'{subpath}/openapi.json', include_in_schema=False)
async def access_openapi():
    openapi = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
    )
    openapi["servers"] = [{"url": app.root_path}]
    return openapi