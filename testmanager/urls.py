"""testmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('candidate/',include('candidate.urls')),
    path('admin/',include('administration.urls')),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('logout/', TemplateView.as_view(template_name='logout.html'), name='logout'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]
