# Generated by Django 3.2 on 2022-05-24 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('works', '0014_alter_productionvideo_youtube_source'),
        ('profiles', '0008_alter_usercomment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='usercomment',
            unique_together={('user', 'production')},
        ),
    ]