from decouple import config as env_config

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env_config("EMAIL_HOST")
EMAIL_PORT = env_config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = env_config("EMAIL_USE_TLS", cast=bool)
EMAIL_USE_SSL = env_config("EMAIL_USE_SSL", cast=bool)
EMAIL_HOST_USER = env_config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env_config("EMAIL_HOST_PASSWORD")
