# Generated by Django 3.2 on 2022-05-16 20:08

from django.db import migrations, models
import works.models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0002_auto_20220516_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='people',
            name='thumb_image',
            field=models.ImageField(blank=True, null=True, upload_to=works.models.people_thumb_image_path),
        ),
    ]
