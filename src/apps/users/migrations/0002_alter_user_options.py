# Generated by Django 4.2.5 on 2023-09-28 01:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
        ),
    ]
