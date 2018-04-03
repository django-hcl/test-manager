from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ..models import *
from django.contrib.auth.models import User

def index(request):
    #return HttpResponseRedirect('/candidate/')
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
            return HttpResponse('else1')
    else:
         return HttpResponseRedirect('/login/')
        #return render(request,'login.html')

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
    user_lists = Customuser.objects.values('custom_userid','custom_userid__username','custom_userid__email','custom_roleid')

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
            return HttpResponseRedirect('/admin/user/add')
    else:
        return render(request, 'administration/user_add.html',{'role_arqument':role_arqument})