from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('login', views.custom_login, name='custom_login'),
     path('logout', views.logout_function, name='logout_function'),
     path('user', views.user_list, name='user_list'),
]