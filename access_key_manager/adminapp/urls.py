from django.urls import path
from adminapp import views
from .views import AccessKeyListView

urlpatterns = [
    path('feed/', AccessKeyListView.as_view(), name='access_key_list'),
    path('generate/', views.access_key_generate, name='access_key_generate'),
]
