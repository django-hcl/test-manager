from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..models import *
from django.db.models import Q
import re
import json
import datetime
from django.urls import reverse
from administration.forms import TestsectionForm, TestForm
from django.core import serializers
from django.db.models import Avg, Max, Min,Count



@login_required
def testlist(request):
    test_value_list = Test.objects.all()
    test_list = sorted(test_value_list, key=lambda Test: Test.test_name)
    return render(request, 'administration/testlist.html', {'test_list': test_list})

@csrf_exempt
@login_required
def addtest(request):
    current_user = request.user.id
    test_list = Testsection.objects.all()
    testsection_record_list = sorted(test_list, key=lambda Testsection:Testsection.section_name)
    duplicate_section_list = Testsection.objects.values('section_name').annotate(Count('section_name')).filter(section_name__count__gt=1)
    if request.method == 'POST':

        form_action = request.POST['form_action']
        test = Test()
        if form_action == 'addtest':
            recordexists = Test.objects.filter(test_name=request.POST.get('testname')).first()
            if recordexists:
                print("entered addtest")
                existingtesterror = True
                return render(request, 'administration/addtest.html',{'existingtesterror': existingtesterror})
            else:
                test.test_name = re.sub(' +', ' ', request.POST.get('testname').strip())
                test.test_name = test.test_name[:1].upper() + test.test_name[1:]
                test.test_description = re.sub(' +', ' ', request.POST.get('testdescription').strip())
                test.created_by = User.objects.get(pk=current_user)
                test.created_date = datetime.datetime.now()
                test.test_duration_mins = request.POST.get('testduration')

                sectionlist = request.POST.getlist('currentsection')
                test.test_sectionid = str(sectionlist).strip("[]")
                test.save()
                return HttpResponseRedirect(reverse('test_list'))
        else:
            print("entered validation else1")
            recordexists = Testsection.objects.filter(section_name=request.POST.get('sectionname'))
            if recordexists:
                existingsectionerror = True
                return render(request, 'administration/addtest.html',{'existingsectionerror': existingsectionerror})
            else:
                print("entered addsection 2")
                section = Testsection()
                section.section_name = re.sub(' +', ' ', request.POST.get('sectionname').strip())
                section.section_description = re.sub(' +', ' ', request.POST.get('sectiondescription').strip())
                section.section_createdby = User.objects.get(pk=current_user)
                section.section_created_date = datetime.datetime.now()
                section.save()
                return HttpResponseRedirect(reverse('add_test'))
    else:
        return render(request, 'administration/addtest.html', {'testsection_record_list': testsection_record_list,
                                                               'duplicate_section_list':duplicate_section_list})



@login_required
def testedit(request, id):
    test = Test.objects.filter(pk=id).first()
    section = Testsection.objects.filter(pk=id).first()
    current_user = request.user.id
    if request.method == "POST":
        testname = [request.POST.get('test_name'), request.POST.get('test_description')]
        test.test_name = testname[0].strip()
        test.test_description = testname[1].strip()
        test.test_modified_by = User.objects.get(id=current_user)
        test.test_modified_date = datetime.datetime.now()
        test.save()
        return HttpResponseRedirect(reverse('test_list'))
    else:
        form = TestForm(instance=test)
        form1 = TestsectionForm(instance=section)
        return render(request, 'administration/testedit.html', {'form': form, 'form1': form1})


@login_required
def testsectionlist(request):
    test_section_list = Testsection.objects.all()
    section_list = sorted(test_section_list, key=lambda Testsection: Testsection.section_name)
    return render(request, 'administration/sectionlist.html', {'section_list': section_list})



@login_required
def addsection(request):
    section = Testsection()
    current_user = request.user.id
    form = TestsectionForm()
    if request.method == 'POST':
        form = TestsectionForm(request.POST)
        if form.is_valid():
            recordexists = Testsection.objects.filter(section_name=request.POST.get('sectionname'))
            if recordexists:
                existingerror = True
                return render(request, 'administration/addsection.html', {'existingerror': existingerror})
            else:
                section.section_name = re.sub(' +', ' ', request.POST.get('section_name').strip())
                section.section_description = re.sub(' +', ' ', request.POST.get('section_description').strip())
                section.section_createdby = User.objects.get(pk=current_user)
                section.section_created_date = datetime.datetime.now()
                section.save()
                return HttpResponseRedirect(reverse('test_section_list'))

    return render(request, 'administration/addsection.html', {'form':form})


@login_required
def sectionedit(request, id):
    section = Testsection.objects.filter(pk=id).first()
    current_user = request.user.id
    if request.method == "POST":
        sectionname = [request.POST.get('section_name'), request.POST.get('section_description')]
        section.section_name = sectionname[0].strip()
        section.section_description = sectionname[1].strip()
        section.section_modified_by = User.objects.get(id=current_user)
        section.section_modified_date = datetime.datetime.now()
        section.save()
        return HttpResponseRedirect(reverse('test_section_list'))
    else:
        form = TestsectionForm(instance=section)
        return render(request, 'administration/sectionedit.html', {'form': form})


@login_required()
@csrf_exempt
def sectiondelete(request):

    data ={}
    id = request.POST['id']
    action = request.POST['action']

    if request.is_ajax():
        section = Testsection.objects.filter(pk=id).first()
        sectionmappingexisting = SectionMapping.objects.filter(Q(sectionmap_sectionid=id) &
                                                               Q(sectionmap_sectionid__is_active=1)).exists()
        if sectionmappingexisting:
            data['messages'] = "You cannot delete this section."
            return HttpResponse(json.dumps(data['messages']))
        else:
            if action == "disable":
                section.is_active = 0
                section.save()
                data['messages'] ="successfully deleted"
                return HttpResponse(json.dumps(data['messages']))
            else:
                section.is_active = 1
                section.save()
                data['messages'] ="successfully enabled"
                return HttpResponse(json.dumps(data['messages']))
    return HttpResponseRedirect(reverse('test_section_list'))


@login_required()
@csrf_exempt
def testdelete(request):
    data ={}
    id = request.POST['id']
    action = request.POST['action']

    if request.is_ajax():
        test = Test.objects.filter(pk=id).first()
        testmappingexisting = TestMapping.objects.filter(Q(testmap_testid=id) &
                                                         Q(testmap_testid__is_active=1)).exists()
        if testmappingexisting:
            data['messages'] = "You cannot delete this test."
            return HttpResponse(json.dumps(data['messages']))
        else:
            if action == "disable":
                test.is_active = 0
                test.save()
                data['messages'] ="successfully deleted"
                return HttpResponse(json.dumps(data['messages']))
            else:
                test.is_active = 1
                test.save()
                data['messages'] ="successfully enabled"
                return HttpResponse(json.dumps(data['messages']))
    return HttpResponseRedirect(reverse('test_list'))



@login_required
def test_asJson(request):
    datadict=dict()
    object_list =list(Test.objects.values())
    datadict['data'] = object_list
    return JsonResponse(datadict,safe=False)


@login_required
def sectionmappinglist(request, id):
    test_section_mappinglist = SectionMapping.objects.filter(sectionmap_testid=id)
    return render(request, 'administration/sectionmappinglist.html', {'test_section_mappinglist': test_section_mappinglist})



