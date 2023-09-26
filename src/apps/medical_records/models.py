from django.db import models
from django.utils.translation import gettext_lazy as _

from src.includes import utils
from src.includes.drf_helpers import (
    UUIDPrimaryKeyMixin,
    BaseValidateMixin,
    DateHistoryMixin,
)


class MedicalRecord(
    UUIDPrimaryKeyMixin,
    BaseValidateMixin,
    DateHistoryMixin,
):
    MRID_PREFIX = "MRN"
    mrid = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        editable=False,
        unique=True,
        help_text=_("Unique Medical Record Public ID"),
    )
    patient = models.ForeignKey(
        "users.PatientProfile",
        on_delete=models.CASCADE,
        related_name="medical_records",
    )
    doctor = models.ForeignKey(
        "users.DoctorProfile",
        on_delete=models.CASCADE,
        related_name="medical_records",
    )
    treatment = models.TextField(
        null=False,
        blank=False,
        help_text=_("Treatment provided by doctor"),
    )
    diagnosis = models.TextField(
        null=False,
        blank=False,
        help_text=_("Diagnosis provided by doctor"),
    )

    class Meta:
        verbose_name = "Medical Record"
        verbose_name_plural = "Medical Records"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["mrid"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
        ]

    def __str__(self):
        return self.mrid

    def _pre_save_init(self):
        self.mrid = utils.generate_sec_id(
            prefix=self.MRID_PREFIX,
            model=MedicalRecord,
            sec_id_field="mrid",
        )
