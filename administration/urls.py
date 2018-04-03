from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('test/edit/<int:id>/', views.testedit, name='testedit'),
     path('test/add', views.addtest, name='add_test'),
     path('test', views.testlist, name='test_list'),
     path('login', views.custom_login, name='custom_login'),
     path('logout', views.logout_function, name='logout_function'),
     path('user', views.user_list, name='user_list'),
]