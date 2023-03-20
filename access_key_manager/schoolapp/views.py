from django.shortcuts import render,redirect, get_objects_or_404,messages
from django.contrib.auth.decorators import login_required
from .models import AccessKey,School

# @login_required
def access_key_list(request):
    school = School.objects.get(name=request.user.school_name)
    access_keys = AccessKey.objects.filter(school=school)
    context = {'access_keys': access_keys}
    return render(request, 'access_key_list.html') 

def key_info(request, school_id):
    school = get_objects_or_404(School, id=school_id)
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
    access_key = get_objects_or_404(AccessKey, assigned_to=request.user)
    active_key = AccessKey.objects.filter(assigned_to=request.user, status='active').first()
    if active_key:
        messages.warning(request, 'You already have an active key')
    else:
        access_key.status = 'active'
        access_key.assigned_to = request.user
        access_key.save()
        messages.success(request, 'Key puchase successful')
    return redirect('key_list')