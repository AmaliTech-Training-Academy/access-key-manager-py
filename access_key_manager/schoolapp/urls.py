from django.urls import path
from .views import access_key_list

urlpatterns = [
    path('access-keys/', access_key_list, name='access_key_list'),
] 
