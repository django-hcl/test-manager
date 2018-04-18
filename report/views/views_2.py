from django.shortcuts import render

# Create your views here.

def index1(request):
    #return HttpResponseRedirect('/candidate/')
    return render(request,'report/index.html')
