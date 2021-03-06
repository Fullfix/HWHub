# Generated by Django 3.0.2 on 2020-03-04 14:26

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200302_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=20, unique=True, validators=[users.validators.validate_input]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=15, validators=[users.validators.validate_input]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='surname',
            field=models.CharField(blank=True, max_length=15, validators=[users.validators.validate_input]),
        ),
    ]
