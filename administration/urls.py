from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name='index'),
     path('test/section/mappinglist/<int:id>/', views.sectionmappinglist, name='section_mapping_list'),
     path('test/section/delete/', views.sectiondelete, name='section_delete'),
     path('test/section/edit/<int:id>/', views.sectionedit, name='section_edit'),
     path('test/section/add', views.addsection, name='add_section'),
     path('test/section', views.testsectionlist, name='test_section_list'),
     path('test/delete/', views.testdelete, name='test_delete'),
     path('test/edit/<int:id>/', views.testedit, name='test_edit'),
     path('test1', views.test_asJson, name='my_ajax_url'),
     path('test/add', views.addtest, name='add_test'),
     path('test', views.testlist, name='test_list'),
     path('login', views.custom_login, name='custom_login'),
     path('logout', views.logout_function, name='logout_function'),
     path('user', views.user_list, name='user_list'),
     path('user/add', views.user_add, name='user_add'),
]