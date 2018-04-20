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

     path('role', views.role_list, name='role_list'),
     path('role/add', views.role_add, name='role_add'),
     path('role/edit/<int:id>/', views.role_edit, name='role_edit'),

     path('user', views.user_list, name='user_list'),
     path('user/add', views.user_add, name='user_add'),
     path('user/edit/<int:id>/', views.user_edit, name='user_edit'),

     path('question', views.question_list, name='question_list'),
     path('question/add', views.question_add, name='question_add'),
     path('question/edit/<int:id>/', views.question_edit, name='question_edit'),
     path('question/choices', views.question_choice_list, name='question_choice_list'),

     path('complexity', views.complexity_list, name='complexity_list'),
     path('complexity/add', views.complexity_add, name='complexity_add'),
     path('complexity/edit/<int:id>/', views.complexity_edit, name='complexity_edit'),

     path('questiontype', views.questiontype_list, name='questiontype_list'),
     path('questiontype/add', views.questiontype_add, name='questiontype_add'),
     path('questiontype/edit/<int:id>/', views.questiontype_edit, name='questiontype_edit'),

]