# Generated by Django 3.2 on 2022-05-19 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_userprofile_default_country'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='default_town_or_city',
            new_name='default_city',
        ),
    ]