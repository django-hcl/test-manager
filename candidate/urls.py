from django.urls import path
from . import views

urlpatterns = [
     path('dashboard', views.dashboard, name='dashboard'),
     path('', views.index, name='index'),
     path('completed', views.completed, name='completed'),
     path('inprogress', views.pending, name='inprogress'),
     path('upcoming', views.upcoming, name='upcoming'),
     path('evaluate/<int:test_id>/', views.evaluate, name='evaluate'),

     path('profile', views.profile, name='profile'),
     path('instruction/<int:id>/', views.instruction, name='instruction'),
     path('exam/<int:id>/', views.exam, name='exam'),
     path('exam_ajax_question/',views.exam2,name='exam_ajax_question'),
     path('exam_ajax_previous_question/',views.exam_previous_question,name='exam_ajax_previous_question'),





]