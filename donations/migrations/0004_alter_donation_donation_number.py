# Generated by Django 3.2 on 2022-05-19 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0003_auto_20220519_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='donation_number',
            field=models.CharField(default='CAD6F6100E7244269EE0E6BB0631E003', max_length=32),
        ),
    ]
