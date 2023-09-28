from rest_framework_simplejwt.tokens import RefreshToken

from src.apps.users import enums as user_enums
from src.apps.users import models as user_models


def authenticate_user(client, user):
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + str(refresh.access_token))


def setup_patients():
    user_one = user_models.User.objects.create_user(
        email="test@mail.com",
        password="Test#1234",
        first_name="Test",
        last_name="Test",
        middle_name="Test",
        gender=user_enums.Gender.MALE,
        role=user_enums.UserRoles.PATIENT,
    )
    patient_one = user_models.PatientProfile.objects.create(
        user=user_one,
        date_of_birth="2000-01-01",
    )

    user_two = user_models.User.objects.create_user(
        email="tester@mail.com",
        password="Sett#1234",
        first_name="Tester",
        last_name="Tester",
        middle_name="Tester",
        gender=user_enums.Gender.FEMALE,
        role=user_enums.UserRoles.PATIENT,
    )
    patient_two = user_models.PatientProfile.objects.create(
        user=user_two,
        date_of_birth="2000-01-02",
    )
    return patient_one, patient_two


def setup_doctors():
    user_one = user_models.User.objects.create_user(
        email="docky@mail.com",
        password="DOCK#1234",
        first_name="docky",
        last_name="docky",
        middle_name="docky",
        gender=user_enums.Gender.MALE,
        role=user_enums.UserRoles.DOCTOR,
    )
    doctor_one = user_models.DoctorProfile.objects.create(
        user=user_one,
        specialization="Cardiologist",
    )

    user_two = user_models.User.objects.create_user(
        email="docksy@mail.com",
        password="DOCKSY#1234",
        first_name="docksy",
        last_name="docksy",
        middle_name="docksy",
        gender=user_enums.Gender.FEMALE,
        role=user_enums.UserRoles.DOCTOR,
    )
    doctor_two = user_models.DoctorProfile.objects.create(
        user=user_two,
        specialization="Neurologist",
    )
    return doctor_one, doctor_two
