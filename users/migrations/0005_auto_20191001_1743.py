# Generated by Django 2.1.5 on 2019-10-01 13:43

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20191001_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(default='users/default.jpg', upload_to=users.models.upload_location),
        ),
    ]
