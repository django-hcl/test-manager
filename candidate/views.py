import sys, traceback
import json
import pdb
from django.core import serializers
from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from administration.models import *
from django.db.models import Q, Max, Min
import random
def dashboard(request):
    return render(request,'dashboard.html')

def index(request):

    try:
        current_user = request.user
        active_test= TestMapping.objects.filter(testmap_userid=current_user,testmap_status__in=(0,3))
        return render(request,'candidate/active.html',{'active_test':active_test})

    except Exception as e:
        exception_line_no = sys.exc_info()[2]
        print(exception_line_no.tb_lineno,e.args)
        return HttpResponseNotFound('<h1>Page not found</h1>')

def instruction(request,id):

    try:
        test_name = TestMapping.objects.filter(pk=id).first()
        return render(request,'candidate/instruction.html',{'test_name':test_name})

    except Exception as e:
        exception_line_no = sys.exc_info()[2]
        print(exception_line_no.tb_lineno,e.args)
        return HttpResponseNotFound('<h1>Page not found</h1>')

def rewrite(request,id):

    try:
        test_name = TestMapping.objects.filter(pk=id).first()
        return render(request,'candidate/exam_rewrite.html',{'test_name':test_name})

    except Exception as e:
        exception_line_no = sys.exc_info()[2]
        print(exception_line_no.tb_lineno,e.args)
        return HttpResponseNotFound('<h1>Page not found</h1>')

def completed(request):

    try:
        current_user = request.user
        completed_test= TestMapping.objects.filter(testmap_userid=current_user,testmap_status__in=(1,2))
        return render(request,'candidate/completed.html',{'completed_test':completed_test})

    except Exception as e:
        exception_line_no = sys.exc_info()[2]
        print(exception_line_no.tb_lineno,e.args)
        return HttpResponseNotFound('<h1>Page not found</h1>')


def upcoming(request):
    return render(request,'candidate/upcoming.html')


def profile(request):

    try:
        userinstance = User.objects.filter(id = request.user.id)
        if request.method == 'POST':
            return render(request,'candidate/profile.html',{'userinstance':userinstance})
        else:
            return render(request,'candidate/profile.html',{'userinstance':userinstance})

    except Exception as e:
        exception_line_no = sys.exc_info()[2]
        print(exception_line_no.tb_lineno,e.args)
        return HttpResponseNotFound('<h1>Page not found</h1>')

@csrf_exempt
def exam(request,id=None):
    try:
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

            test_status_object =TestMapping.objects.get(testmap_userid=current_user,testmap_testid=id)
            test_status_object.testmap_status=3
            test_status_object.save()
        return render(request,'candidate/exam.html',{'questionchoices':questionchoices,'test':test,'choices':choices})
    except Exception as e:
        exception_line_no = sys.exc_info()[2]
        print(exception_line_no.tb_lineno,e.args)
        return HttpResponseNotFound('<h1>Page not found</h1>')

@csrf_exempt
def exam2(request):

    try:
        current_user = request.user
        user = User.objects.get(username=current_user)
        if request.is_ajax():
            response={}
            temp_tbl_id = request.POST['temp_tbl_id']
            candidate_choices= request.POST.getlist("choicetext[]")

            temp_tabl = TempTable.objects.filter(temp_id=temp_tbl_id).first()
            test_id = Test.objects.filter(pk = temp_tabl.temptable_test.test_id ).first()
            question = Question.objects.filter(question_id = temp_tabl.temptable_question.question_id ).first()
            tmpresponse_question = TempResponse.objects.filter(choice_question__question_id = question.question_id )
            if not candidate_choices:
                pass
            else:
                if(TempResponse.objects.filter(choice_question__question_id = question.question_id ).count() >1 or len(candidate_choices)>1):
                     TempResponse.objects.filter(choice_question__question_id = question.question_id ).delete()
                     tmpresponse_question = TempResponse.objects.filter(choice_question__question_id = question.question_id )
                for eachchoice in candidate_choices:
                    print("eachchoice "+str(eachchoice))
                    if tmpresponse_question:
                        #update choice
                        tmpresponse = TempResponse.objects.get(choice_question__question_id = question.question_id )
                        tmpresponse.choice_text = eachchoice
                        tmpresponse.save()
                    else:
                        #new entry
                        tmpresponse = TempResponse()
                        tmpresponse.temp_response_user = user
                        tmpresponse.choice_question = question
                        tmpresponse.choice_text = eachchoice
                        tmpresponse.temp_response_test = test_id
                        tmpresponse.save()
            #next or previous question
            button_action = request.POST['button_action']
            if button_action == "next_btn":
                temp_id_to_pick = int(temp_tbl_id)+1

            elif button_action == "back_btn":
                temp_id_to_pick =  int(temp_tbl_id)-1
            if button_action != "submit_btn":

                question_id_pick = TempTable.objects.filter(temp_id=temp_id_to_pick).first()

                choices = QuestionChoice.objects.filter(choice_question__question_id=question_id_pick.temptable_question.question_id)
                response['question'] = question_id_pick.temptable_question.question_text
                response['choices'] = [ choice.choice_text for choice in choices ]
                response['choice_type'] = question_id_pick.temptable_question.question_type.questiontype_name
                response['temp_id'] =  question_id_pick.temp_id
                response['test_id'] = test_id.test_id

                tmpresponse_question = TempResponse.objects.filter(choice_question__question_id = question_id_pick.temptable_question.question_id )


                response['saved_choice'] = ""
                if tmpresponse_question:
                    saved_choice=[]
                    for eachchoice in tmpresponse_question:
                        saved_choice.append(eachchoice.choice_text)
                    response['saved_choice'] =saved_choice

                response['show_next_btn']= TempTable.objects.filter(temp_id=temp_id_to_pick+1).exists()
                response['show_back_btn']= TempTable.objects.filter(temp_id=temp_id_to_pick-1).exists()
                print("response"+str(response))

            serializeddata = json.dumps(response)
            return HttpResponse(serializeddata, content_type='application/json')

    except Exception as e:
        exception_line_no = sys.exc_info()[2]
        print(exception_line_no.tb_lineno,e.args)
        return HttpResponseNotFound('<h1>Page not found</h1>')



def evaluate(request,test_id):
   try:

        current_user = request.user
        user = User.objects.filter(username = current_user).first()
        temp_response_list =TempResponse.objects.filter(temp_response_user__id=user.id, temp_response_test__test_id=test_id)\
            .values('choice_question__question_id').distinct()

        marks=0
        correct_answers=0
        result_list={}
        print(temp_response_list)
        for temp_resp in temp_response_list:
            print()
            for key,value in temp_resp.items():


                if key == 'choice_question__question_id':
                    temp_count= TempResponse.objects.filter(choice_question__question_id=value, temp_response_test__test_id=test_id).count()
                    question_count= QuestionChoice.objects.filter(choice_question__question_id=value,choice_is_correct=True).count()

                    if temp_count == question_count:
                        temp_response =TempResponse.objects.filter(choice_question__question_id=value, temp_response_test__test_id=test_id)\
                         .values('choice_question__question_id', 'choice_text').distinct()
                        ques_choice_list = QuestionChoice.objects.filter(choice_question__question_id=value,choice_is_correct=True)\
                         .values('choice_question__question_id', 'choice_text')

                        count=0
                        for x in ques_choice_list:
                            if x in temp_response:
                              count=count+1
                              #print(count)
                            else:
                                break
                        if  len(ques_choice_list)==count:
                            print(len(ques_choice_list))
                            print(count)
                            print()
                            correct_answers=correct_answers+1
                            print(correct_answers)


        total_questions = len(set(TempTable.objects.all()))
        candidate_percentage =int((correct_answers / total_questions)*100)
        test_status_object=TestMapping.objects.get(testmap_userid=current_user,testmap_testid=test_id)
        if candidate_percentage > 75:
            test_status_object.testmap_status = 1
            result = "Pass"
        else:
            test_status_object.testmap_status = 2
            result = "Fail"
        test_status_object.save()
        TempTable.objects.all().delete()
        TempResponse.objects.all().delete()

        return render(request,'candidate/evaluate.html',{'correct_answers':correct_answers,'result':result,'total_questions':total_questions})

     except Exception as e:
              return render(request,'candidate/evaluate.html')

