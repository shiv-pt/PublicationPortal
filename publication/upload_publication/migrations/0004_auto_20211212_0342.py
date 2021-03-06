# Generated by Django 3.2.5 on 2021-12-11 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload_publication', '0003_auto_20211212_0335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paper_has_references',
            old_name='ISSN_ID',
            new_name='ISSN',
        ),
        migrations.RenameField(
            model_name='paper_has_references',
            old_name='P_ID',
            new_name='PAPER_ID',
        ),
        migrations.AlterUniqueTogether(
            name='paper_has_references',
            unique_together={('PAPER_ID', 'ISSN')},
        ),
    ]
