from django.shortcuts import render

# Create your views here.

def chart(request):
    #return HttpResponseRedirect('/candidate/')
    return render(request,'report/index.html')

def index(request):
    #return HttpResponseRedirect('/candidate/')
    return render(request,'report/theme.html')