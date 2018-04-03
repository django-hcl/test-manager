from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from ..models import *
import re
import datetime

@login_required
def testlist(request):
    test_value_list = Test.objects.all()
    test_list = sorted(test_value_list, key=lambda Test: Test.test_name)
    return render(request, 'administration/testlist.html', {'test_list': test_list})


@login_required
def testedit(request, id):
    test_list = Test.objects.filter(pk=id)
    request.session['temp_test_id'] = id
    return render(request, 'administration/testedit.html', {'test_list': test_list})


@login_required
def addtest(request):
    test_list = Testsection.objects.all()
    testsection_record_list = sorted(test_list, key=lambda Testsection:Testsection.section_name)
    if request.method == 'POST':

        form_action = request.POST['form_action']
        test = Test()
        if form_action == 'addtest':
            test.test_name = re.sub(' +', ' ', request.POST.get('testname').strip())
            test.test_name = test.test_name[:1].upper() + test.test_name[1:]
            test.test_description = re.sub(' +', ' ', request.POST.get('testdescription').strip())
            test.test_createdby = User.objects.get(id=2)
            test.test_createdon = datetime.datetime.now()
            test.test_duration_mins = request.POST.get('testduration')

            sectionlist = request.POST.getlist('currentsection')
            test.test_sectionid = str(sectionlist).strip("[]")

            test.save()
            return HttpResponseRedirect('/admin/test')
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
    if request.method == 'POST':
        section.section_name = re.sub(' +', ' ', request.POST.get('sectionname').strip())
        section.section_createdby = User.objects.get(id=2)
        section.section_createdon = datetime.datetime.now()
        section.save()
        return HttpResponseRedirect('/admin/test/section')
    else:
        return render(request, 'administration/addsection.html')


@login_required
def sectionedit(request, id):
    testsection_list = Testsection.objects.filter(pk=id)
    request.session['temp_section_id'] = id
    return render(request, 'administration/sectionedit.html', {'test_list': testsection_list})


