from django import forms
from .models import School


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name']
    def save(self, commit=True):
        name = super().save(commit=False)
        if commit:
            name.save()
        return name

