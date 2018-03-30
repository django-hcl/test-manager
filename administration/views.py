from .models import Test, Testsection
import re
import datetime
from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import Role,Customuser
from django.contrib.auth.models import User

# Create your views here.


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
            return HttpResponseRedirect('/admin/')
        else:
            return HttpResponse('else1')
    else:
         return HttpResponseRedirect('/login/')
        #return render(request,'login.html')


def logout_function(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def user_list(request):
    user_lists = Customuser.objects.values('custom_userid','custom_userid__username','custom_userid__email','custom_roleid')

    return render(request, 'administration/user_list.html',{'user_lists': user_lists})


def testlist(request):
    test_value_list = Test.objects.all()
    test_list = sorted(test_value_list, key=lambda Test: Test.test_name)
    return render(request, 'administration/testlist.html', {'test_list': test_list})


def testdetails(request, test_id):
    pass


def addtest(request):
    if request.method == 'POST':
        test = Test()
        test.test_name = re.sub(' +', ' ', request.POST.get('testname').strip())
        test.test_name = test.test_name[:1].upper() + test.test_name[1:]
        test.test_description = re.sub(' +', ' ', request.POST.get('testdescription').strip())
        test.test_createdon = datetime.datetime.now()
        test.test_duration_mins = request.POST.get('testduration')
        test.test_createdby = User.objects.get(id=2)
        test.save()
        return HttpResponseRedirect('/admin/test')
    else:
        return render(request, 'administration/addtest.html')

