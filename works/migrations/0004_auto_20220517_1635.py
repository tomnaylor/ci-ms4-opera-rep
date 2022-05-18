# Generated by Django 3.2 on 2022-05-17 16:35

from django.db import migrations, models
import django.db.models.deletion
import works.models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0003_people_thumb_image'),
    ]

    operations = [

        migrations.CreateModel(
            name='ProductionPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('full_image', models.ImageField(blank=True, null=True, upload_to=works.models.production_photo_full_image_path)),
                ('thumb_image', models.ImageField(blank=True, null=True, upload_to=works.models.production_photo_thumb_image_path)),
                ('record_added', models.DateTimeField(auto_now_add=True)),
                ('record_edited', models.DateTimeField(auto_now=True)),
                ('rating_total', models.PositiveIntegerField(blank=True, null=True)),
                ('rating_count', models.PositiveIntegerField(blank=True, null=True)),
                ('production', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='works.production')),
            ],
        ),
    ]
