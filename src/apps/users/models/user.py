from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from src.includes.drf_helpers import (
    UUIDPrimaryKeyMixin,
    DateHistoryMixin,
)

from src.apps.users.enums import Gender, UserRoles
from src.apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, UUIDPrimaryKeyMixin, DateHistoryMixin):
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    middle_name = models.CharField(_("middle name"), max_length=150, blank=True)
    email = models.EmailField(
        _("email address"),
        unique=True,
        null=False,
        blank=False,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    gender = models.CharField(
        max_length=10, choices=Gender.choices, null=False, blank=False
    )
    role = models.CharField(
        max_length=10, choices=UserRoles.choices, null=True, blank=False
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
