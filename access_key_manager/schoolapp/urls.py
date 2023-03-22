from django.urls import path

from schoolapp import views
app_name = 'schoolapp'

urlpatterns = [
    path('access-keys/<int:user_id>/',views.access_key_list, name='access_key_list'),
    path('school/', views.school_view, name='school')
] 
