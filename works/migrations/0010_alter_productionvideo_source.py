# Generated by Django 3.2 on 2022-05-18 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0009_auto_20220518_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionvideo',
            name='source',
            field=models.TextField(max_length=2000),
        ),
    ]
