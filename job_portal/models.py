from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_job_finder = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
class JobFinderProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add additional fields for job finder profile

class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add additional fields for employer profile
