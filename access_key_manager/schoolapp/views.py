from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from adminapp.models import AccessKey
from .models import School
from .forms import SchoolForm
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from authentication.tokens import account_activation_token
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site


@login_required
def access_key_list(request,user_id):
    user = request.user 
    school = get_object_or_404(School, id=user_id)
    access_keys = AccessKey.objects.filter(school=school)
    context = {'access_keys': access_keys, 
               'school': school,
                'user': user,
                }
    return render(request, 'access_key_list.html',context) 



def purchase_key(request,school_id):
    active_key = AccessKey.objects.filter(assigned_to=request.user, status='active').first()
    if active_key:
        messages.warning(request, 'You already have an active key')
    else:
        user = request.user
        current_site = get_current_site(request)
        message=render_to_string('message.html', {
            'user':user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        print(user)
        message = strip_tags(message)
        mail_subject = 'Access Key Request'
        email_from = user.email
        recipient_list=["douglasdanso66@gmail.com"]
        send_mail(mail_subject, message, email_from, recipient_list)
    return render(request,'requests.html',{'school': school_id})

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
