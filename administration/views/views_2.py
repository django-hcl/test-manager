from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from ..models import *
import re
import datetime
from django.urls import reverse
from administration.forms import TestsectionForm



@login_required
def testlist(request):
    test_value_list = Test.objects.all()
    test_list = sorted(test_value_list, key=lambda Test: Test.test_name)
    return render(request, 'administration/testlist.html', {'test_list': test_list})


@login_required
def testedit(request, id):
    test_list = Test.objects.filter(pk=id)
    request.session['temp_test_id'] = id
    return render(request,'administration/testedit.html', {'test_list': test_list})


@login_required
def addtest(request):
    current_user = request.user.id
    print(current_user)
    test_list = Testsection.objects.all()
    testsection_record_list = sorted(test_list, key=lambda Testsection:Testsection.section_name)
    if request.method == 'POST':

        form_action = request.POST['form_action']
        test = Test()
        if form_action == 'addtest':
            test.test_name = re.sub(' +', ' ', request.POST.get('testname').strip())
            test.test_name = test.test_name[:1].upper() + test.test_name[1:]
            test.test_description = re.sub(' +', ' ', request.POST.get('testdescription').strip())
            test.test_createdby = User.objects.get(pk=current_user)
            test.test_createdon = datetime.datetime.now()
            test.test_duration_mins = request.POST.get('testduration')
            sectionlist = request.POST.getlist('currentsection')
            test.test_sectionid = str(sectionlist).strip("[]")
            test.save()
            return HttpResponseRedirect(reverse('test_list'))
        else:
            return render(request, 'administration/addtest.html')

    else:
        return render(request, 'administration/addtest.html', {'testsection_record_list': testsection_record_list})


@login_required
def testsectionlist(request):
    test_section_list = Testsection.objects.all()
    section_list = sorted(test_section_list, key=lambda Testsection: Testsection.section_name)
    return render(request, 'administration/sectionlist.html', {'section_list': section_list})


@login_required
def addsection(request):
    section = Testsection()
    current_user = request.user.id
    if request.method == 'POST':
        recordexists = Testsection.objects.filter(section_name=request.POST.get('sectionname'))
        if recordexists:
            existingerror = True
            return render(request, 'administration/addsection.html', {'existingerror': existingerror})
        else:
            section.section_name = re.sub(' +', ' ', request.POST.get('section_name').strip())
            section.section_description = re.sub(' +', ' ', request.POST.get('section_description').strip())
            section.section_createdby = User.objects.get(pk=current_user)
            section.section_createdon = datetime.datetime.now()
            section.save()
            return HttpResponseRedirect(reverse('test_section_list'))
    else:
        form = TestsectionForm()
        return render(request, 'administration/addsection.html', {'form':form})


@login_required
def sectionedit(request, id):
    section = Testsection.objects.filter(pk=id).first()
    current_user = request.user.id
    if request.method == "POST":
        sectionname = [request.POST.get('section_name'), request.POST.get('section_description')]
        section.section_name = sectionname[0].strip()
        section.section_description = sectionname[1].strip()
        section.section_createdby = User.objects.get(id=current_user)
        section.section_createdon = datetime.datetime.now()
        section.save()
        return HttpResponseRedirect(reverse('test_section_list'))
    else:
        form = TestsectionForm(instance=section)
        return render(request, 'administration/sectionedit.html', {'form': form})


