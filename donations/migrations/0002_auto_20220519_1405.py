# Generated by Django 3.2 on 2022-05-19 14:05

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation',
            name='county',
        ),
        migrations.AlterField(
            model_name='donation',
            name='country',
            field=django_countries.fields.CountryField(default='GB', max_length=2),
        ),
        migrations.AlterField(
            model_name='donation',
            name='donation_number',
            field=models.CharField(default='56A1EDB41EF6442990049DCD23C5367F', editable=False, max_length=32),
        ),
    ]
