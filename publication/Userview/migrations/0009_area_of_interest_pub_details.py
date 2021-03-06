# Generated by Django 3.2.5 on 2021-12-12 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Userview', '0008_publisher_paper'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pub_Details',
            fields=[
                ('PUBD_ID', models.AutoField(primary_key=True, serialize=False)),
                ('SCOPUS_ID', models.CharField(max_length=20)),
                ('PUBLON_ID', models.CharField(max_length=20)),
                ('H_INDEX', models.IntegerField()),
                ('I_INDEX', models.IntegerField()),
                ('ORCHID', models.CharField(max_length=20)),
                ('publisher', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Userview.publisher')),
            ],
            options={
                'db_table': 'PUB_DETAILS',
            },
        ),
        migrations.CreateModel(
            name='Area_of_interest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('INTEREST', models.CharField(max_length=70)),
                ('SAP_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Userview.publisher')),
            ],
            options={
                'db_table': 'AREA_OF_INTEREST',
            },
        ),
    ]
