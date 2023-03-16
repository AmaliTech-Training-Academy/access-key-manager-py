from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AccessKey,School

@login_required
def access_key_list(request):
    school = School.objects.get(name=request.user.school_name)
    access_keys = AccessKey.objects.filter(school=school)
    context = {'access_keys': access_keys}
    return render(request, 'access_key_list.html') 






