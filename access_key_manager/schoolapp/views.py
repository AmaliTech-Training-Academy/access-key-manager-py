from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from adminapp.models import AccessKey
from .models import School
from .forms import SchoolForm
from authentication.tokens import account_activation_token
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from adminapp.views import access_key_generate
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden,HttpResponse

@login_required
def access_key_list(request,school_id):
    user = request.user 
    school = get_object_or_404(School, id=school_id)
    access_keys = AccessKey.objects.filter(school=school)
    paginator = Paginator(access_keys, 5) #

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'access_keys': access_keys, 
               'school': school,
                'user': user,
                'page_obj':page_obj,
                }
    return render(request, 'access_key_list.html',context) 

@login_required
def purchase_key(request, school_id):
    school = School.objects.get(id=school_id)
    active_key = AccessKey.objects.filter(school=school, status=AccessKey.ACTIVE).first()

    if active_key:
        messages.warning(request, 'you already have an active access key')
        return redirect('schoolapp:access_key_list', school_id=school.id)
    else:
        return redirect('adminapp:access_key_generate', school_id=school.id)
    
@login_required
def requests(request, school_id):
    school = School.objects.get(id= school_id)
    return render(request, 'requests.html',{'school':school})

@login_required
def school_view(request):
    form = SchoolForm()

    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['school_name']

            user = request.user
            school = School.objects.create(school_name=name, user=user)
            school.save()
            return redirect('schoolapp:access_key_list', school_id=school.id)
        else:
            form = SchoolForm()

    return render(request, 'school.html', {'form':form})

