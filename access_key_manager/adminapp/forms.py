from django import forms
from django.utils import timezone
import datetime
from authentication.models import CustomUser
from .models import AccessKey
import random,string


class AccessKeyForm(forms.ModelForm):
    class Meta:
        model = AccessKey
        fields = ['expiry_date']

    def save(self, commit=True):
        access_key = super().save(commit=False)
        access_key.key = self.generate_key()
        
        # if access_key.expiry_date and access_key.expiry_date < datetime.date.today():
        #     raise forms.ValidationError('Expiry date cannot be in the past.')
        # else:
        access_key.expiry_date = self.cleaned_data['expiry_date']
       
        if commit:
            access_key.save()
        return access_key

    def generate_key(self):
        # Generate a random 64-character string for the key
        return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=32))

# class AccessKeyForm(forms.ModelForm):
#     class Meta:
#         model = AccessKey
#         fields = ['expiry_date']

#     def save(self, commit=True):
#         access_key = super().save(commit=False)
#         access_key.key = self.generate_key()
#         access_key.expiry_date = self.clean_expiry_date()
        
#         if commit:
#             access_key.save()
#         return access_key

#     def generate_key(self):
#         # Generate a random 64-character string for the key
#         return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=32))

#     def clean_expiry_date(self):
#         expiry_date = self.cleaned_data['expiry_date']
#         if expiry_date and expiry_date < datetime.date.today():
#             raise forms.ValidationError('Expiry date cannot be in the past.')
#         return expiry_date

    
class EmailForm(forms.Form):
    email = forms.EmailField(max_length=200)