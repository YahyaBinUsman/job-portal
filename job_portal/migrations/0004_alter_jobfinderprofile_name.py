# Generated by Django 5.0.6 on 2024-07-14 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0003_jobfinderprofile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobfinderprofile',
            name='name',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
