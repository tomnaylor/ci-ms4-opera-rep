# Generated by Django 3.2 on 2022-05-19 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0013_auto_20220518_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionvideo',
            name='youtube_source',
            field=models.CharField(blank=True, help_text='https://www.youtube.com/embed/', max_length=100, null=True),
        ),
    ]