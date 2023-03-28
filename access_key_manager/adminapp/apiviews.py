from rest_framework.views import APIView
from django.http import Http404
from .models import AccessKey
from rest_framework.response import Response
from rest_framework import status 
from django.shortcuts import get_object_or_404,render
from .serializers import AccessKeySerializer
from .forms import EmailForm
from authentication.models import CustomUser
from schoolapp.models import School


def get_email(request):
        form = EmailForm()
        if request.method == 'post':
            form = EmailForm(request.Post)
            if form.is_valid:
                email = form.cleaned_data['email']
                try:
                    user = CustomUser.objects.get(email=email)
                
                except user.DoesNotExist:
                    form.add_error(None, 'Email address not found, try again')
            else:
                form = EmailForm()
        return render(request, 'adminapp/email_api_form.html', {'form': form})

class GetActiveAccessKey(APIView):
    
    def get(self,request):
        email = get_email(request)
        user = CustomUser.objects.get(email=email)
        school = School.objects.get(user = user)
        if email:
            try:
                    # access_key = AccessKey. get_object_or_404(email=email, status=AccessKey.ACTIVE)
                access_key = get_object_or_404(AccessKey,  status=AccessKey.ACTIVE ,school= school)
                
            except AccessKey.DoesNotExist:
                raise Http404    
        serializer = AccessKeySerializer(access_key)
        return Response(serializer.data)