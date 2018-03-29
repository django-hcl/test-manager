from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request,'candidate/index.html')