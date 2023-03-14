from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import AccessKey
from .forms import AccessKeyForm
from django.contrib import messages

# @method_decorator(login_required, name='dispatch')
class AccessKeyListView(ListView):
    model = AccessKey
    template_name = 'adminapp/access_key_list.html'
    context_object_name = 'access_keys'
    paginate_by = 20

# @login_required
def access_key_generate(request):
    if request.method == 'POST':
        form = AccessKeyForm(request.POST)
        if form.is_valid():
            access_key = form.save()
            return redirect('access_key_list')
    else:
        form = AccessKeyForm()
    return render(request, 'adminapp/access_key_generate.html', {'form': form})

# @login_required
def access_key_revoke(request):


