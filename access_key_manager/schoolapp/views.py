from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from adminapp.models import AccessKey
from .models import School
from .forms import SchoolForm
from django.core.paginator import Paginator


@login_required
def access_key_list(request,school_id):
    user = request.user 
    school = get_object_or_404(School, id=school_id)
    access_keys = AccessKey.objects.filter(school=school).order_by('-date_of_procurement')
    paginator = Paginator(access_keys, 1) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    paginate_by = 2
    context = { 
               'school': school,
                'user': user,
                'page_obj':page_obj,
                }
    return render(request, 'access_key_list.html',context) 

@login_required
def purchase_key(request, school_id):
    school = School.objects.get(id=school_id)
    active_key = AccessKey.objects.filter(school=school, status=AccessKey.ACTIVE)

    if active_key:
        messages.warning(request, 'you already have an active access key')
        return redirect('schoolapp:access_key_list', school_id=school.id)
    else:
        return redirect('adminapp:access_key_generate', school_id=school.id)
    

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

#"// code for paginator with maximum 20 items per page in django"?

