from django import forms
from .models import School
from authentication.models import CustomUser
from adminapp.models import AccessKey
from django.shortcuts import get_object_or_404


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name']

    def save(self, commit=True):
        name = super().save(commit=False)
        if commit:
            key = get_object_or_404(AccessKey,school=name)
            user = get_object_or_404(CustomUser,id = user.id)
            school_profile = School(name = name, activekey = key, user = user, )
            school_profile.save()
        
    def clean(self):
        cleaned_data = super().clean()
        name = self.cleaned_data.get('name')
        return cleaned_data
