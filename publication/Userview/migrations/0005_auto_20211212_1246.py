# Generated by Django 3.2.5 on 2021-12-12 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_publication', '0007_delete_paper_has_references'),
        ('Userview', '0004_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='papers',
            field=models.ManyToManyField(to='upload_publication.Papers'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='ISSUEP_ID',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
