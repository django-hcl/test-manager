from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from administration.models import Customuser,Test

# Create your views here.

def index(request):
    #return render(request,'candidate/index.html')
    return HttpResponseRedirect('/candidate/dashboard')
def dashboard(request):
    return render(request,'dashboard.html')
def activePage(request):
    test= Customuser.objects.filter(custom_userid_id=2)
    for val in test:
        value=val.custom_assignedtest
        value2=Test.objects.filter(test_id=value)
    return render(request,'candidate/active.html',{'tests':value2})
def pending(request):
    return render(request,'candidate/inprogress.html')
def completed(request):
    return render(request,'candidate/completed.html')
def upcoming(request):
    return render(request,'candidate/upcoming.html')