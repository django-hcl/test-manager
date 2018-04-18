from django.urls import path
from . import views

urlpatterns = [
     path('dashboard', views.dashboard, name='dashboard'),
     path('', views.index, name='index'),
     path('completed', views.completed, name='completed'),
     path('inprogress', views.pending, name='inprogress'),
     path('upcoming', views.upcoming, name='upcoming'),
]