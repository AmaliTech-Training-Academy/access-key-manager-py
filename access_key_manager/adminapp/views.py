from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import AccessKey
from schoolapp.models import School
from .forms import AccessKeyForm,EmailForm
from django.contrib import messages
import datetime
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from authentication.models import CustomUser
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from authentication.tokens import account_activation_token
from django.utils.encoding import force_str
from django.core.mail import send_mail

# @method_decorator(login_required, name='dispatch')
class AccessKeyListView(ListView):
    model = AccessKey
    template_name = 'adminapp/dashboard.html'
    context_object_name = 'access_keys'
    paginate_by = 20


# @login_required
def access_key_generate(request,school_id):
    schools = get_object_or_404(School, id=school_id)
    form = AccessKeyForm()

    if request.method == 'POST':
        form = AccessKeyForm(request.POST)
        if form.is_valid():
            form.save()

            mail_subject = "Access Key for {school.name}"
            message = f"Your access key for {schools.name} is {access_key.key}."
            email_from = "douglasdanso66@gmail.com"
            recipient_list = [schools.email]
            send_mail(mail_subject, message, email_from, recipient_list)
                
            return redirect('adminapp:access_key_list')
        else:
            form = AccessKeyForm()
    context = {
        'form':form,
        'schools':schools,
    }  
    return render(request, 'adminapp/access_key_generate.html', context)

# @login_required
def revoke_key(request, access_key_id):
    access_key = get_object_or_404(AccessKey, id=access_key_id)
    access_key.status = 'revoked'
    access_key.save()
    # if access_key.school.active_key == access_key:
    #     access_key.school.active_key = None
    #     access_key.school.save()
    messages.success(request, 'Key revoked successfully.')
    return redirect('adminapp:access_key_list')

# @login_required
def access_key_update(request, access_key_id):
    access_key = get_object_or_404(AccessKey, pk=access_key_id)

    if request.method == 'POST':
        form = AccessKeyForm(request.POST, instance=access_key)
        if form.is_valid():
            access_key = form.save()
            messages.success(request, f'Access key {access_key.key} has been updated.')
            return redirect('adminapp:access_key_list')
    else:
        form = AccessKeyForm(instance=access_key)

    return render(request, 'adminapp/access_key_update.html', {'form': form, 'access_key': access_key})

# @login_required
# @csrf_exempt
# def get_active_access_key(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         if email:
#             try:
#                 access_key = AccessKey.objects.get(email=email, status=AccessKey.ACTIVE)
#                 response_data = {
#                     'access_key': access_key.key,
#                     'expiry_date': access_key.expiry_date.isoformat(),
#                 }
#                 return JsonResponse(response_data, status=200)
#             except AccessKey.DoesNotExist:
#                 pass
#     return HttpResponseNotFound()
    
    


