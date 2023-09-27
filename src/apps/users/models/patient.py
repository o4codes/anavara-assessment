from django.db import models
from django.utils.translation import gettext_lazy as _

from src.includes.drf_helpers import (
    UUIDPrimaryKeyMixin,
    BaseValidateMixin,
)
from src.includes import utils


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
