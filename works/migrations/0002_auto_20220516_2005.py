# Generated by Django 3.2 on 2022-05-16 20:05

from django.db import migrations, models
import works.models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='people',
            name='hero_image_url',
        ),
        migrations.RemoveField(
            model_name='people',
            name='thumb_image_url',
        ),
        migrations.AddField(
            model_name='people',
            name='hero_image',
            field=models.ImageField(blank=True, null=True, upload_to=works.models.people_hero_image_path),
        ),
        migrations.AlterField(
            model_name='production',
            name='hero_image',
            field=models.ImageField(blank=True, null=True, upload_to=works.models.production_hero_image_path),
        ),
        migrations.AlterField(
            model_name='production',
            name='thumb_image',
            field=models.ImageField(blank=True, null=True, upload_to=works.models.production_thumb_image_path),
        ),
    ]
