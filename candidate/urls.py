from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('dashboard', views.dashboard, name='dashboard'),
     path('active', views.activePage, name='active'),
     path('completed', views.completed, name='completed'),
     path('inprogress', views.pending, name='inprogress'),
     path('upcoming', views.upcoming, name='upcoming'),
]