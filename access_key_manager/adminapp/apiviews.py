from rest_framework.views import APIView
from django.http import Http404
from .models import AccessKey
from rest_framework.response import Response
from rest_framework import status 
from django.shortcuts import get_object_or_404,render
from .serializers import AccessKeySerializer
from .forms import EmailForm


def get_email(request):
        form = EmailForm()
        if request.method == 'post':
            form = EmailForm(request.Post)
            if form.is_valid:
                api_email = form.cleaned_data['email']
                api_email.save()
            else:
                form = EmailForm()
        return render(request, 'adminapp/email_api_form.html', {'form': form})

class GetActiveAccessKey(APIView):
    
    def get(request,api_email):
        # if request.method == 'POST':
        #     email = request.POST.get('email')
        if api_email:
            try:
                    # access_key = AccessKey. get_object_or_404(email=email, status=AccessKey.ACTIVE)
                access_key = get_object_or_404(AccessKey,  status=AccessKey.ACTIVE )
                
            except AccessKey.DoesNotExist:
                raise Http404    
        serializer = AccessKeySerializer(access_key)
        return Response(serializer.data)