from decouple import config as env_config
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from src.apps.users.enums import Gender, UserRoles
from src.apps.users.managers import UserManager
from src.includes.drf_helpers import DateHistoryMixin, UUIDPrimaryKeyMixin


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

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def send_email(
        self,
        context: dict,
        subject: str,
        message: str,
        template: str = None,
    ):
        from django.core.mail import send_mail

        html_message = None
        if template:
            html_message = render_to_string(
                template,
                context,
            )
        return send_mail(
            subject=subject,
            message=message,
            from_email=env_config("EMAIL_HOST_USER", default="admin@anavara.com"),
            recipient_list=[self.email],
            html_message=html_message,
        )
