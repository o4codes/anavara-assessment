from datetime import timedelta
from decouple import config as env_config

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=env_config("ACCESS_TOKEN_LIFETIME", cast=int, default=15)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=env_config("REFRESH_TOKEN_LIFETIME", cast=int, default=1)
    ),
}
