# Generated by Django 3.2 on 2022-05-19 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0002_auto_20220519_1405'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donation',
            old_name='town_or_city',
            new_name='city',
        ),
        migrations.AlterField(
            model_name='donation',
            name='donation_number',
            field=models.CharField(default='8BE3BE9FF3F74205918E80E0088F7589', max_length=32),
        ),
    ]
