# Generated by Django 2.1.5 on 2019-09-29 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0003_auto_20190925_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='book',
            field=models.CharField(choices=[['algebra10profile2', 'РђР»РіРµР±СЂР° 10 РєР»Р°СЃСЃ РїСЂРѕС„РёР»СЊРЅС‹Р№ СѓСЂРѕРІРµРЅСЊ С‡Р°СЃС‚СЊ 2']], max_length=30),
        ),
    ]
