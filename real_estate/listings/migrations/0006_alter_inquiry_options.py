# Generated by Django 5.2 on 2025-06-01 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_category_created_at_category_updated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inquiry',
            options={'verbose_name_plural': 'Inquiries'},
        ),
    ]
