# Generated by Django 5.0.6 on 2024-07-13 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0002_alter_employerprofile_company_description_friendlist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobfinderprofile',
            name='name',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
