
import json
import pdb
from django.core import serializers
from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from administration.models import *
from django.db.models import Q, Max, Min
import random
def dashboard(request):
    return render(request,'dashboard.html')

def index(request):
    current_user = request.user
    active_test= TestMapping.objects.filter(testmap_userid=current_user)
    return render(request,'candidate/active.html',{'active_test':active_test})


def instruction(request,id):

    test_name = TestMapping.objects.filter(pk=id).first()
    return render(request,'candidate/instruction.html',{'test_name':test_name})

def pending(request):
    return render(request,'candidate/inprogress.html')
def completed(request):
    return render(request,'candidate/completed.html')
def upcoming(request):
    return render(request,'candidate/upcoming.html')

def profile(request):

    userinstance = User.objects.filter(id = request.user.id)
    #return HttpResponse(userinstance)

    if request.method == 'POST':

        return render(request,'candidate/profile.html',{'userinstance':userinstance})
    else:
        return render(request,'candidate/profile.html',{'userinstance':userinstance})

@csrf_exempt
def exam(request,id=None):
    if not request.is_ajax():
        current_user = request.user
        data ={}
        simplequestionslist=[]
        mediumquestionlist=[]
        complexquestionlist=[]
        sectionmapping = SectionMapping.objects.filter(sectionmap_testid__test_id=id)
        user = User.objects.filter(username = current_user).first()
        test = Test.objects.filter(test_id= id).first()
        for eachsectionmappingvalue in sectionmapping:
            section_questions = Question.objects.filter(question_section__section_id=eachsectionmappingvalue.sectionmap_sectionid.section_id)
            for eachsectionquestion in section_questions:
               complexity1 = Question.objects.filter(Q(question_id =eachsectionquestion.question_id ) & Q(question_complex__complex_name="Simple")).first()
               complexity2 = Question.objects.filter(Q(question_id =eachsectionquestion.question_id ) & Q(question_complex__complex_name="Medium")).first()
               complexity3 = Question.objects.filter(Q(question_id =eachsectionquestion.question_id ) & Q(question_complex__complex_name="Complex")).first()
               if(complexity1):
                    simplequestionslist.append(complexity1.question_text)
               if(complexity2):
                   mediumquestionlist.append(complexity2.question_text)
               if(complexity3):
                   complexquestionlist.append(complexity3.question_text)
            simplequestionslist =random.sample(simplequestionslist,2)
            mediumquestionlist = random.sample(mediumquestionlist,2)
            complexquestionlist = random.sample(complexquestionlist,2)
            totallist = simplequestionslist+mediumquestionlist+complexquestionlist
            data[eachsectionmappingvalue.sectionmap_sectionid.section_name] = totallist
            for eachlist in totallist:
                question = Question.objects.filter(question_text= eachlist).first()
                testsection = Testsection.objects.filter(section_id= eachsectionmappingvalue.sectionmap_sectionid.section_id).first()
                tmptable=TempTable()
                if not TempTable.objects.filter(temptable_test__test_id = test.test_id ,temptable_question__question_text=eachlist).exists():
                    tmptable.temptable_userid = user
                    tmptable.temptable_question = question
                    tmptable.temptable_section = testsection
                    tmptable.temptable_test = test
                    tmptable.save()
        temp_tabl = TempTable.objects.filter(temptable_userid = user,temptable_test = test).order_by('temp_id')[0]
        choices  = QuestionChoice.objects.filter(choice_question__question_id=temp_tabl.temptable_question.question_id)
        questionchoices={}
        questionchoices['question'] = temp_tabl.temptable_question
        questionchoices['choices'] = [ choice.choice_text for choice in choices ]
        questionchoices['choice_type'] = temp_tabl.temptable_question.question_type.questiontype_name
        questionchoices['temp_id'] =  temp_tabl.temp_id
    return render(request,'candidate/exam.html',{'questionchoices':questionchoices,'test':test,'choices':choices})


@csrf_exempt
def exam2(request):
     if request.is_ajax():
            questionchoices={}
            id = request.POST['value']
            current_user = request.user
            temp_tabl = TempTable.objects.filter(temp_id=id).first()
            if temp_tabl == None:
                questionchoices['temp_table_empty'] = True
            else:
                test_id = Test.objects.filter(pk = temp_tabl.temptable_test.test_id ).first()
                candidate_choices= request.POST.getlist("choicetext[]")

                question = Question.objects.filter(pk = temp_tabl.temptable_question.question_id ).first()
                user = User.objects.get(username=current_user)
                for eachchoice in candidate_choices:
                    tmpresponse = TempResponse()
                    tmpresponse.temp_response_user = user
                    tmpresponse.choice_question = question
                    tmpresponse.choice_text = eachchoice
                    tmpresponse.temp_response_test = test_id
                    tmpresponse.save()
                choices = QuestionChoice.objects.filter(choice_question__question_id=temp_tabl.temptable_question.question_id)


                questionchoices['question'] = temp_tabl.temptable_question.question_text

                questionchoices['choices'] = [ choice.choice_text for choice in choices ]
                questionchoices['choice_type'] = temp_tabl.temptable_question.question_type.questiontype_name
                questionchoices['temp_id'] =  temp_tabl.temp_id
                questionchoices['test_id'] = test_id.test_id
            serializeddata = json.dumps(questionchoices)

            return HttpResponse(serializeddata, content_type='application/json')

def evaluate(request,test_id):
    ques_choice = []
    sample=[]
    current_user = request.user
    user = User.objects.filter(username = current_user).first()
    temp_response_list =TempResponse.objects.filter(temp_response_user__id=user.id, temp_response_test__test_id=test_id)\
        .values('choice_question__question_id', 'choice_text')
    print(temp_response_list)
    for temp_resp in temp_response_list:
        for key,value in temp_resp.items():
            if key == 'choice_question__question_id':
                ques_choice_list = QuestionChoice.objects.filter(choice_question__question_id=value, choice_is_correct=True)\
                 .values('choice_question__question_id', 'choice_text')
                choice_list = [x for x in temp_response_list if x in ques_choice_list ]
                if choice_list:
                    sample.append(choice_list)
                ques_choice.append(ques_choice_list)
    total_questions = len(temp_response_list)
    correct_answers = len(sample)
    candidate_percentage =int((correct_answers / total_questions)*100)
    if candidate_percentage > 60:
        result = "Pass"
    else:
        result = "Fail"

    TempResponse.objects.all().delete()
    TempTable.objects.all().delete()

    return render(request,'candidate/evaluate.html',{'correct_answers':correct_answers,'result':result,'total_questions':total_questions})



