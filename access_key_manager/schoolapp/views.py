from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from adminapp.models import AccessKey
from .models import School
from .forms import SchoolForm
from authentication.models import CustomUser
# @login_required
def access_key_list(request,school_id):
    school = get_object_or_404(School, id=school_id)
    access_keys = AccessKey.objects.filter(school=school)
    context = {'access_keys': access_keys}
    return render(request, 'access_key_list.html',context) 

def key_info(request, school_id):
    school = get_object_or_404(School, id=school_id)
    keys = AccessKey.objects.filter(school=school)

    key_info_list = []
    for key in keys:
        key_info = key.school_key_info(school)
        if key_info:
            key_info_list.append(key_info)

    context = {
        'school': school,
        'key_info_list': key_info_list,
    }
    return render(request, 'key_info.html', context)

def purchase_key(request):
    access_key = get_object_or_404(AccessKey, assigned_to=request.user)
    active_key = AccessKey.objects.filter(assigned_to=request.user, status='active').first()
    if active_key:
        messages.warning(request, 'You already have an active key')
    else:
        access_key.status = 'active'
        access_key.assigned_to = request.user
        access_key.save()
        messages.success(request, 'Key puchase successful')
    return redirect('key_list')

def school_view(request):
    user = CustomUser.objects.get(pk=request.user.pk)
    form = SchoolForm()
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            user = request.user
            name = user
            name.save()
            redirect('access_key_list')
        else:
            form = SchoolForm()

    return render(request, 'school.html', {'form':form})
