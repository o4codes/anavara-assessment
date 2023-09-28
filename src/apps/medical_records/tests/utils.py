from src.apps.medical_records import models as medical_records_models
from src.apps.users import models as user_models


def setup_medical_record(
    patient: user_models.PatientProfile,
    doctor: user_models.DoctorProfile,
):
    medical_record = medical_records_models.MedicalRecord.objects.create(
        doctor=doctor,
        patient=patient,
        diagnosis="Diagnosis of Malaria",
        treatment="Use of Panadol",
    )
    return medical_record
