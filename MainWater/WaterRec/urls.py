from django.urls import path

from . import views

app_name = 'water'
urlpatterns = [

    path('sendphoto', views.recievephoto, name='recieve'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('resetpassword/', views.ResetPassword.as_view(), name='resetpassword'),
    path('checkdefaultpassword/', views.CheckDefaultPassword.as_view(), name='checkdefaultpassword'),
    path('service/', views.ServiceRecord.as_view(), name='service'),
    path('counters/', views.Counters.as_view(), name='counters'),
    path('meterdata/<int:id_counter>', views.NewAndLastMetersData.as_view(), name='meterdata'),


]