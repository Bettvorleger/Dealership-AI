import os

if os.environ.get("DATABASE_URL"):
    TORTOISE_ORM = {
        "connections": {"default": os.environ.get("DATABASE_URL")},
        "apps": {
            "models": {
                "models": [
                    "src.database.models", "aerich.models"
                ],
                "default_connection": "default"
            }
        }
    }
else:
    TORTOISE_ORM = {
        "connections": {"default": "postgres://test"},
        "apps": {
            "models": {
                "models": [
                    "src.database.models", "aerich.models"
                ],
                "default_connection": "default"
            }
        }
    }
