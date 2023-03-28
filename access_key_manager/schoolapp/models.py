from django.db import models
from django.conf import settings
from authentication.models import CustomUser
from adminapp.models import AccessKey

class School(models.Model):
    name = models.CharField(max_length=100)
    active_key = models.ForeignKey(AccessKey, null=True, blank=True, on_delete=models.SET_NULL, related_name='school')
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.school.name
              





