# Generated by Django 3.2.5 on 2021-12-19 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_publication', '0012_auto_20211214_2006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authors',
            name='F_NAME',
        ),
        migrations.RemoveField(
            model_name='authors',
            name='L_NAME',
        ),
        migrations.RemoveField(
            model_name='authors',
            name='M_NAME',
        ),
        migrations.AddField(
            model_name='authors',
            name='A_NAME',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AddField(
            model_name='reference',
            name='RANKING',
            field=models.CharField(blank=True, default='N/A', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='papers',
            name='doi',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
