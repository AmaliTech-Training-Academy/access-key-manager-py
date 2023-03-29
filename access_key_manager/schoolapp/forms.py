from django import forms
from .models import School
from authentication.models import CustomUser
from adminapp.models import AccessKey
from django.shortcuts import get_object_or_404


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['school_name']

   
