from django.shortcuts import render
# from .models import AccessKey

# def access_key_list(request):
#     access_keys = AccessKey.objects.all()
#     return render(request, 'access_key_list.html', {'access_keys': access_keys})

# def purchase_key(request, access_key_id):
#     access_key = get_object_or_404(AccessKey, pk=access_key_id)
#     if access_key.status == 'active':
#         messages.success(request, 'Key revoked successfully.')
#     else:

