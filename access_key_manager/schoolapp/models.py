from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class School(models.Model):
    name = models.CharField(max_length=100)

class AccessKey(models.Model):
    ACCESS_KEY_STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    ]
    key = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=ACCESS_KEY_STATUS_CHOICES, default='active')
    date_of_procurement = models.DateField()
    expiry_date = models.DateField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)



