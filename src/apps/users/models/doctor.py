from django.db import models
from django.utils.translation import gettext_lazy as _

from src.includes.drf_helpers import (
    UUIDPrimaryKeyMixin,
    BaseValidateMixin,
)
from src.includes import utils


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
