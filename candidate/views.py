from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from administration.models import Customuser,Test,TestMapping

# Create your views here.


   # return HttpResponseRedirect('/candidate/dashboard')
def dashboard(request):
    return render(request,'dashboard.html')

def index(request):
    current_user = request.user
    print(current_user.id)
    test= TestMapping.objects.filter(testmap_userid=current_user)

    return render(request,'candidate/active.html',{'tests':test})

def pending(request):
    return render(request,'candidate/inprogress.html')
def completed(request):
    return render(request,'candidate/completed.html')
def upcoming(request):
    return render(request,'candidate/upcoming.html')