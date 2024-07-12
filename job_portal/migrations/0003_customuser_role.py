# Generated by Django 5.0.6 on 2024-07-12 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_portal', '0002_bid_job_jobapplication_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('job_finder', 'Job Finder'), ('employer', 'Employer')], default='job_finder', max_length=20),
        ),
    ]
