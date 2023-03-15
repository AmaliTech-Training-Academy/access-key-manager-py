from django.urls import path
from adminapp import views
from .views import AccessKeyListView

urlpatterns = [
    path('feed/', AccessKeyListView.as_view(), name='access_key_list'),
    path('generate/', views.access_key_generate, name='access_key_generate'),
    path('update/<int:access_key_id>/', views.access_key_update, name='access_key_update'),
    path('access_key/<int:access_key_id>/revoke/', views.revoke_key, name='access_key_revoke'),
]
