# Generated by Django 3.2.5 on 2021-12-19 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Userview', '0013_alter_publisher_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='LAST_NAME',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
    ]
