# Generated by Django 3.2.5 on 2021-12-12 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upload_publication', '0010_remove_papers_papers'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='paper',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='upload_publication.papers'),
        ),
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('F_NAME', models.CharField(max_length=15)),
                ('M_NAME', models.CharField(blank=True, max_length=15)),
                ('L_NAME', models.CharField(blank=True, max_length=15)),
                ('PAPER_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload_publication.papers')),
            ],
            options={
                'db_table': 'AUTHORS',
            },
        ),
    ]
