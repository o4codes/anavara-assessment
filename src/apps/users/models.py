from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from src.includes.drf_helpers import (
    UUIDPrimaryKeyMixin,
    BaseValidateMixin,
    DateHistoryMixin,
)
from src.includes import utils
from .enums import Gender, UserRoles
from .managers import UserManager


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


class PatientProfile(UUIDPrimaryKeyMixin, BaseValidateMixin):
    UHID_PREFIX = "PAT"
    uhid = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        editable=False,
        unique=True,
        help_text=_("Unique Patient Public ID"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient")
    date_of_birth = models.DateField(null=True)

    class Meta:
        verbose_name = "Patient Profile"
        verbose_name_plural = "Patient Profiles"
        ordering = ["-user__created_at"]

    def __str__(self):
        return self.uhid

    def _pre_save_init(self):
        self.uhid = utils.generate_sec_id(
            prefix=self.UHID_PREFIX,
            model=PatientProfile,
            sec_id_field="uhid",
        )


class DoctorProfile(UUIDPrimaryKeyMixin, BaseValidateMixin):
    UMID_PREFIX = "DOC"
    umid = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        editable=False,
        unique=True,
        help_text=_("Unique Doctor Public ID"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor")
    specialization = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        help_text=_("Doctor Specialization"),
    )

    class Meta:
        verbose_name = "Doctor Profile"
        verbose_name_plural = "Doctor Profiles"
        ordering = ["-user__created_at"]

    def __str__(self):
        return self.umid

    def _pre_save_init(self):
        self.umid = utils.generate_sec_id(
            prefix=self.UMID_PREFIX,
            model=DoctorProfile,
            sec_id_field="umid",
        )
