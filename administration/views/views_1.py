from django.core.serializers import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ..models import *
from django.contrib.auth.models import User
from administration.forms import CustomUserForm,UserForm
from django.urls import reverse


def index(request):
    return render(request,'administration/index.html')

def custom_login(request):

    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            if is_admin(request, user):
                return HttpResponseRedirect('/admin/')
            else:
                return HttpResponseRedirect('/candidate/')
        else:
            login_error = True
            return render(request, 'login.html',{'login_error': login_error})

    else:
         return HttpResponseRedirect('/login/')

def is_admin(request, user):
    user_lists = Customuser.objects.filter(custom_userid=user).values('custom_roleid')
    if user_lists and user_lists[0]['custom_roleid'] == 1:
        return True
    else:
        return False


@login_required
def logout_function(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_required
def user_list(request):
    user_lists = Customuser.objects.values('id','custom_userid','custom_userid__username','custom_userid__email','custom_roleid')

    return render(request, 'administration/user_list.html',{'user_lists': user_lists})

@login_required
def user_add(request):

    role_instance = Role.objects.all()
    role_arqument = sorted(role_instance, key = lambda Role:Role.role_description)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        emailid = request.POST['emailid']
        roleid = request.POST['roleid']
        if not (User.objects.filter(username=username).exists()):
                User.objects.create_user(username, emailid, password)
                Customuser_instance = Customuser()
                Customuser_instance.custom_userid = User.objects.latest('id')
                Customuser_instance.custom_roleid = Role.objects.get(role_id=roleid)
                Customuser_instance.save()
                return HttpResponseRedirect('/admin/user')
        else:
            useradd_error = True
            return render(request, 'administration/user_add.html',{'role_arqument':role_arqument,'useradd_error':useradd_error})
    else:
        return render(request, 'administration/user_add.html',{'role_arqument':role_arqument})




def user_edit(request, id):
    user = User.objects.filter(pk = id ).first()
    customuser = Customuser.objects.filter(custom_userid =user.id).first()
    user_form = UserForm()
    customuserform = CustomUserForm()
    if request.method == 'POST':
        customform = CustomUserForm(request.POST)
        userform = UserForm(request.POST)
        role = Role.objects.filter(pk = request.POST["custom_roleid"]).first()
        customuser.custom_userid = user
        customuser.custom_roleid = role
        customuser.save()
        user.username = request.POST["username"]
        user.email = request.POST['email']
        user.save()
        return HttpResponseRedirect(reverse('user_list'))
    else:
       customuserform = CustomUserForm(instance=customuser)
       user_form = UserForm(instance=user)

    return render(request, 'administration/user_edit.html', {'user_form': user_form,'customuserform': customuserform})
