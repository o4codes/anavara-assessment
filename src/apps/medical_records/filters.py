import django_filters

from .models import MedicalRecord


class MedicalRecordFilter(django_filters.FilterSet):
    class Meta:
        model = MedicalRecord
        fields = ["mrid"]

    mrid = django_filters.CharFilter(field_name="mrid", lookup_expr="icontains")
    patient_first_name = django_filters.CharFilter(
        field_name="patient__user__first_name", lookup_expr="icontains"
    )
    patient_last_name = django_filters.CharFilter(
        field_name="patient__user__last_name", lookup_expr="icontains"
    )
    patient_email = django_filters.CharFilter(
        field_name="patient__user__email", lookup_expr="icontains"
    )
    doctor_first_name = django_filters.CharFilter(
        field_name="doctor__user__first_name", lookup_expr="icontains"
    )
    doctor_last_name = django_filters.CharFilter(
        field_name="doctor__user__last_name", lookup_expr="icontains"
    )
    doctor_email = django_filters.CharFilter(
        field_name="doctor__user__email", lookup_expr="icontains"
    )
    date_range = django_filters.DateFromToRangeFilter(
        field_name="created_at",
    )
