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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class GetActiveAccessKey(APIView):
    
    def get(self, request):
        form = EmailForm(request.GET or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                school = School.objects.get(user=user)
                access_key = AccessKey.objects.get(status=AccessKey.ACTIVE, school=school)
                serializer = AccessKeySerializer(access_key)
                return Response(serializer.data)
            except (CustomUser.DoesNotExist, School.DoesNotExist, AccessKey.DoesNotExist):
                raise Http404
        return render(request, 'adminapp/email_api_form.html', {'form': form})