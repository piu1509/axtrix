# Generated by Django 4.1.5 on 2023-04-13 05:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("department", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Job",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "gid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("slug", models.SlugField(unique=True)),
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "organization",
                    models.UUIDField(blank=True, default=uuid.uuid4, null=True),
                ),
                (
                    "job_poster",
                    models.UUIDField(blank=True, default=uuid.uuid4, null=True),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("experience", models.CharField(blank=True, max_length=255, null=True)),
                ("salary", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "skills_required",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("address", models.CharField(blank=True, max_length=400, null=True)),
                ("vacancies", models.IntegerField(blank=True, null=True)),
                (
                    "qualifications",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
