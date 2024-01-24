# Generated by Django 4.1.5 on 2023-04-12 06:21

from django.db import migrations, models
import modules.venture.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated')),
                ('date_deleted', models.DateTimeField(auto_now=True, verbose_name='Date deleted')),
                ('gid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=modules.venture.models.organisation_media_path)),
                ('website', models.CharField(max_length=250, unique=True)),
                ('founder', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('founded_on', models.DateField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('contact_no', models.CharField(blank=True, max_length=14, null=True)),
                ('headquarter', models.CharField(blank=True, max_length=250, null=True)),
                ('organisation_type', models.CharField(blank=True, max_length=50, null=True)),
                ('area_served', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Organisations',
                'ordering': ('founded_on',),
            },
        ),
    ]