# Generated by Django 3.2.5 on 2021-12-27 17:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Userview', '0017_alter_issue_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='RESPONSE',
        ),
        migrations.AlterField(
            model_name='issue',
            name='TIME_S',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='LAST_NAME',
            field=models.CharField(max_length=100),
        ),
    ]
