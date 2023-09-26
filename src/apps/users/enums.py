from django.db import models


class UserRoles(models.TextChoices):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"


class Gender(models.TextChoices):
    MALE = "MALE"
    FEMALE = "FEMALE"
