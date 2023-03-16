from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import AccessKey
from .forms import AccessKeyForm
from django.contrib import messages
import datetime
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

# @method_decorator(login_required, name='dispatch')
class AccessKeyListView(ListView):
    model = AccessKey
    template_name = 'adminapp/dashboard.html'
    context_object_name = 'access_keys'
    paginate_by = 20

# @login_required
def access_key_generate(request):
    if request.method == 'POST':
        form = AccessKeyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminapp:access_key_list')
    else:
        form = AccessKeyForm()
    return render(request, 'adminapp/access_key_generate.html', {'form': form})

# @login_required
def revoke_key(request, key_id):
    access_key = get_object_or_404(AccessKey, id=key_id)
    access_key.status = 'revoked'
    access_key.save()
    if access_key.school.active_key == access_key:
        access_key.school.active_key = None
        access_key.school.save()
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
@csrf_exempt
def get_active_access_key(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                access_key = AccessKey.objects.get(email=email, status=AccessKey.ACTIVE)
                response_data = {
                    'access_key': access_key.key,
                    'expiry_date': access_key.expiry_date.isoformat(),
                }
                return JsonResponse(response_data, status=200)
            except AccessKey.DoesNotExist:
                pass
    return HttpResponseNotFound()
        