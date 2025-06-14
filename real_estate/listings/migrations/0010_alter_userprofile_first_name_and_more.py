# Generated by Django 5.2 on 2025-06-05 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0009_userprofile_first_name_userprofile_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
