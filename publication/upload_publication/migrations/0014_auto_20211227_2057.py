# Generated by Django 3.2.5 on 2021-12-27 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_publication', '0013_auto_20211219_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='papers',
            name='doi',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='papers',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='papers/pdfs/'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='RANKING',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='SCOPUS_INDEX',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='WEB_OF_SCIENCE',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
