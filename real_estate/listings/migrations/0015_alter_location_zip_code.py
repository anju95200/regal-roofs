# Generated by Django 5.2 on 2025-06-11 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0014_alter_location_zip_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='zip_code',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
