# Generated by Django 4.2.5 on 2023-09-26 17:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MedicalRecord",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "mrid",
                    models.CharField(
                        editable=False,
                        help_text="Unique Medical Record Public ID",
                        max_length=20,
                        unique=True,
                    ),
                ),
                (
                    "treatment",
                    models.TextField(help_text="Treatment provided by doctor"),
                ),
                (
                    "diagnosis",
                    models.TextField(help_text="Diagnosis provided by doctor"),
                ),
            ],
            options={
                "verbose_name": "Medical Record",
                "verbose_name_plural": "Medical Records",
                "ordering": ["-created_at"],
            },
        ),
    ]