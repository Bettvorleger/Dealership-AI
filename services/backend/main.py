from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

# enable schemas to read relationship between models
Tortoise.init_models(["src.database.models"], "models")

# must be AFTER tortoise model init, otherwise foregin keys aren't loadded
from src.routes import users, cars

# set subpath for ingress controller since backend/frontend use same port
subpath = '/fastapi'
app = FastAPI(docs_url=f'{subpath}/docs', openapi_url=f'{subpath}/openapi.json')

# allow API calls from all origins, not the safest option, but convenient :)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# set all router to use the subpath
app.include_router(users.router, prefix=subpath)
app.include_router(cars.router, prefix=subpath)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)

# friendly greeting
@app.get(f'{subpath}/',response_class=PlainTextResponse)
def home():
    return """
    Hello and welcome to:
  _____             _               _     _                  _____ 
 |  __ \           | |             | |   (_)           /\   |_   _|
 | |  | | ___  __ _| | ___ _ __ ___| |__  _ _ __      /  \    | |  
 | |  | |/ _ \/ _` | |/ _ \ '__/ __| '_ \| | '_ \    / /\ \   | |  
 | |__| |  __/ (_| | |  __/ |  \__ \ | | | | |_) |  / ____ \ _| |_ 
 |_____/ \___|\__,_|_|\___|_|  |___/_| |_|_| .__/  /_/    \_\_____|
                                           | |                     
                                           |_|                     
"""
