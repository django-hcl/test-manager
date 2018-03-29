from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('test/add', views.addtest, name='add_test'),
     path('test', views.testlist, name='test_list'),
     path('login', views.custom_login, name='custom_login'),

]