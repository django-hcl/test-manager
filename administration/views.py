from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request,'administration/index.html')

def custom_login(request):
    print(request)
    if request.method == "POST":
        return render(request,'administration/index.html')
    else:
        return HttpResponse("else")
