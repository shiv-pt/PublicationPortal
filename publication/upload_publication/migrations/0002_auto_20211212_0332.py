# Generated by Django 3.2.5 on 2021-12-11 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_publication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='PUB_YEAR',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='reference',
            name='VOL',
            field=models.IntegerField(),
        ),
    ]