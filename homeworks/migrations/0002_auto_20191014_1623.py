# Generated by Django 2.1.5 on 2019-10-14 12:23

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homeworks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='homework',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='homework',
            name='publication_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
