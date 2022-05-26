# Generated by Django 3.2 on 2022-05-24 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_remove_userprofile_default_county'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='default_country',
            new_name='country',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_city',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_phone_number',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_postcode',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_street_address1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_street_address2',
        ),
    ]