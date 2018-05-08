from django.shortcuts import render
from django.core.serializers import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ..models import *
from django.contrib.auth.models import User
from administration.forms import CustomUserForm,UserForm, QuestionAddForm, ComplexityForm, QuestionTypeForm, RoleForm
from django.urls import reverse
import re
import json
from django.core import serializers

def index(request):
    return render(request,'administration/index.html')

def custom_login(request):

    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            if is_admin(request, user):
                return HttpResponseRedirect('/admin/')
            else:
                return HttpResponseRedirect('/candidate/')
        else:
            login_error = True
            return render(request, 'login.html',{'login_error': login_error})
    else:
         return HttpResponseRedirect('/login/')

def is_admin(request, user):
    user_lists = Customuser.objects.filter(custom_userid=user).values('custom_roleid__role_name')
    if user_lists and user_lists[0]['custom_roleid__role_name'] == "Admin":
        return True
    else:
        return False

@login_required
def logout_function(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_required
def role_add(request):
    role_add_list = Role()

    if request.method == 'POST':
        role_exists = Role.objects.filter(role_name = request.POST.get('role_name'))

        if role_exists:
            role_exists_error = True
            return render(request, 'administration/role_add.html', {'role_exists_error': role_exists_error})

        else:
            role_add_list.role_name = re.sub(' +', ' ', request.POST.get('role_name').strip())
            role_add_list.role_name = role_add_list.role_name[:1].upper() + role_add_list.role_name[1:]
            role_add_list.role_description = re.sub(' +', ' ', request.POST.get('role_description').strip())
            role_add_list.role_description = role_add_list.role_description[:1].upper() + role_add_list.role_description[1:]
            role_add_list.save()
            return HttpResponseRedirect(reverse('role_list'))
    else:
        role_form = RoleForm()
        return render(request, 'administration/role_add.html',{'role_form': role_form})

@login_required
def role_list(request):
    list = Role.objects.all()
    role_list = sorted(list, key = lambda Role:Role.role_id)
    return render(request, 'administration/role_list.html',{'role_list': role_list})

@login_required
def role_edit(request,id):

    role_list = Role.objects.filter(pk=id).first()

    if request.method == 'POST':
        role_list.role_name = re.sub(' +', ' ', request.POST.get('role_name').strip())
        role_list.role_name = role_list.role_name[:1].upper() + role_list.role_name[1:]
        role_list.role_description = re.sub(' +', ' ', request.POST.get('role_description').strip())
        role_list.role_description = role_list.role_description[:1].upper() + role_list.role_description[1:]
        role_list.created_by = User.objects.get(id = request.user.id)
        role_list.save()
        return HttpResponseRedirect(reverse('role_list'))

    else:
        role_form = RoleForm(instance = role_list )
        return render(request, 'administration/role_edit.html', {'role_form': role_form})

@login_required
def user_list(request):
    user_lists = Customuser.objects.values('custom_userid','custom_userid__username','custom_userid__email','custom_roleid','created_by')
    return render(request, 'administration/user_list.html',{'user_lists': user_lists})

@login_required
def user_add(request):

    role_instance = Role.objects.all()
    role_arqument = sorted(role_instance, key = lambda Role:Role.role_description)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        emailid = request.POST['emailid']
        roleid = request.POST['roleid']
        if not (User.objects.filter(username=username).exists()):
                User.objects.create_user(username, emailid, password)
                Customuser_instance = Customuser()
                Customuser_instance.custom_userid = User.objects.latest('id')
                Customuser_instance.custom_roleid = Role.objects.get(role_id=roleid)
                Customuser_instance.created_by = User.objects.get(id = request.user.id)
                Customuser_instance.save()
                return HttpResponseRedirect('/admin/user')
        else:
            useradd_error = True
            return render(request, 'administration/user_add.html',{'role_arqument':role_arqument,'useradd_error':useradd_error})
    else:
        return render(request, 'administration/user_add.html',{'role_arqument':role_arqument})

@login_required
def user_edit(request, id):
    user = User.objects.filter(pk = id ).first()
    customuser = Customuser.objects.filter(custom_userid =user.id).first()
    user_form = UserForm()
    customuserform = CustomUserForm()
    if request.method == 'POST':
        customform = CustomUserForm(request.POST)
        userform = UserForm(request.POST)
        role = Role.objects.filter(pk = request.POST["custom_roleid"]).first()
        customuser.custom_userid = user
        customuser.custom_roleid = role
        customuser.save()
        user.username = request.POST["username"]
        user.email = request.POST['email']
        user.save()
        return HttpResponseRedirect(reverse('user_list'))
    else:
       customuserform = CustomUserForm(instance=customuser)
       user_form = UserForm(instance=user)

    return render(request, 'administration/user_edit.html', {'user_form': user_form,'customuserform': customuserform})

@login_required
def question_add(request):

    question_add = Question()

    if request.method == 'POST':

        question_exists = Question.objects.filter(question_text = request.POST.get('question_text'))

        if question_exists:
            question_exists_error = True
            return render(request, 'administration/question_add.html', {'question_exists_error': question_exists_error})
        else:
            complex = Complexity.objects.filter(pk = request.POST["question_complex"]).first()
            ques_type = QuestionType.objects.filter(pk = request.POST["question_type"]).first()
            selection = Testsection.objects.filter(pk = request.POST["question_section"]).first()
            question_add.question_text = re.sub(' +', ' ', request.POST.get('question_text').strip())
            question_add.question_complex = complex
            question_add.question_type = ques_type
            question_add.question_section = selection
            question_add.created_by = User.objects.get(id = request.user.id)
            question_add.save()

            if ques_type.questiontype_id != 3:

                choice_val = request.POST.getlist('choices[]')
                choice_text_len = request.POST.getlist('choices_text')

                for x in choice_text_len:
                    question_choice_add = QuestionChoice()
                    question_choice_add.choice_question = Question.objects.latest('question_id')
                    is_correct_answer = x in choice_val
                    choices_text_param = 'choices_text_'+str(x)
                    question_choice_add.choice_text = request.POST.get(choices_text_param)
                    question_choice_add.choice_is_correct = is_correct_answer
                    question_choice_add.save()
            return HttpResponseRedirect(reverse('question_list'))
    else:
        questionadd_form = QuestionAddForm()
        return render(request, 'administration/question_add.html',{'questionadd_form': questionadd_form})

@login_required
def question_list(request):
    list = Question.objects.all()
    question_list = sorted(list, key = lambda Question:Question.question_text)
    return render(request, 'administration/question_list.html',{'question_list': question_list})

@login_required
def question_edit(request, id):

    question = Question.objects.filter(pk=id).first()

    if request.method == 'POST':

        complex = Complexity.objects.filter(pk = request.POST["question_complex"]).first()
        ques_type = QuestionType.objects.filter(pk = request.POST["question_type"]).first()
        selection = Testsection.objects.filter(pk = request.POST["question_section"]).first()

        question.question_text = re.sub(' +', ' ', request.POST.get('question_text').strip())
        question.question_complex = complex
        question.question_type = ques_type
        question.question_section = selection
        question.save()

        if ques_type.questiontype_id != 3:
            question_choice = QuestionChoice.objects.filter(choice_question= question).delete()
            choice_val = request.POST.getlist('choices[]')
            choice_text_len = request.POST.getlist('choices_text')
            for x in choice_text_len:
                    question_choices = QuestionChoice()
                    question_choices.choice_question = question
                    is_correct_answer = x in choice_val
                    print(is_correct_answer)
                    choices_text_param = 'choices_text_'+str(x)
                    question_choices.choice_text = request.POST.get(choices_text_param)
                    question_choices.choice_is_correct = is_correct_answer
                    question_choices.save()
        return HttpResponseRedirect(reverse('question_list'))

    else:
        question_edit_form = QuestionAddForm(instance=question)

        question_choice = QuestionChoice.objects.filter(choice_question = question)
        choice_list_array =[]
        for choice_row in question_choice:
            choice_list_array_row = {}
            choice_list_array_row['question_id']=choice_row.choice_question.question_id
            choice_list_array_row['choice_id']=choice_row.choice_id
            choice_list_array_row['choice_text']=choice_row.choice_text
            choice_list_array_row['is_correct']=choice_row.choice_is_correct
            choice_list_array_row['question_type']=choice_row.choice_question.question_type.questiontype_id
            choice_list_array.append(choice_list_array_row)
            print(choice_list_array)
        #choice_json_array =  serializers.serialize('json', choice_list_array)
        #choice_json_array =   choice_list_array
        choice_json_array =  json.dumps(choice_list_array)
        return render(request, 'administration/question_edit.html', {'question_edit_form': question_edit_form ,'question_choice':choice_json_array})

@login_required
def question_choice_list(request):
    list = QuestionChoice.objects.all()
    question_choice_list = sorted(list, key = lambda QuestionChoice:QuestionChoice.choice_id)
    return render(request, 'administration/questionchoice_list.html',{'question_choice_list': question_choice_list})

@login_required
def complexity_add(request):
    complexity_add_list = Complexity()
    if request.method == 'POST':
        complexity_exists = Complexity.objects.filter(complex_name = request.POST.get('complex_name'))

        if complexity_exists:
            complexity_exists_error = True
            return render(request, 'administration/complexity_add.html', {'complexity_exists_error': complexity_exists_error})
        else:
            complexity_add_list.complex_name = re.sub(' +', ' ', request.POST.get('complex_name').strip())
            complexity_add_list.complex_name = complexity_add_list.complex_name[:1].upper() + complexity_add_list.complex_name[1:]
            complexity_add_list.complex_description = re.sub(' +', ' ', request.POST.get('complex_description').strip())
            complexity_add_list.complex_description = complexity_add_list.complex_description[:1].upper() + complexity_add_list.complex_description[1:]
            complexity_add_list.save()
            return HttpResponseRedirect(reverse('complexity_list'))

    else:
        complexity_form = ComplexityForm()
        return render(request, 'administration/complexity_add.html',{'complexity_form': complexity_form})

@login_required
def complexity_list(request):
    list = Complexity.objects.all()
    complexity_list = sorted(list, key = lambda Complexity:Complexity.complex_id)
    return render(request, 'administration/complexity_list.html',{'complexity_list': complexity_list})

@login_required
def complexity_edit(request, id):

    complexity_list = Complexity.objects.filter(pk=id).first()

    if request.method == 'POST':
        complexity_list.complex_name = request.POST["complex_name"]
        complexity_list.complex_description = request.POST["complex_description"]
        complexity_list.created_by = User.objects.get(id = request.user.id)
        complexity_list.save()
        return HttpResponseRedirect(reverse('complexity_list'))

    else:
        complexity_edit_form = ComplexityForm(instance=complexity_list)
        return render(request, 'administration/complexity_edit.html', {'complexity_edit_form': complexity_edit_form})

@login_required
def questiontype_add(request):
    question_type_add_list = QuestionType()

    if request.method == 'POST':
        question_type_exists = QuestionType.objects.filter(questiontype_name = request.POST.get('questiontype_name'))

        if question_type_exists:
            question_type_exists_error = True
            return render(request, 'administration/questiontype_add.html', {'question_type_exists_error': question_type_exists_error})

        else:
            question_type_add_list.questiontype_name = re.sub(' +', ' ', request.POST.get('questiontype_name').strip())
            question_type_add_list.questiontype_name = question_type_add_list.questiontype_name[:1].upper() + question_type_add_list.questiontype_name[1:]
            question_type_add_list.questiontype_description = re.sub(' +', ' ', request.POST.get('questiontype_description').strip())
            question_type_add_list.questiontype_description = question_type_add_list.questiontype_description[:1].upper() + question_type_add_list.questiontype_description[1:]
            question_type_add_list.save()
            return HttpResponseRedirect(reverse('questiontype_list'))
    else:
        question_type_form = QuestionTypeForm()
        return render(request, 'administration/questiontype_add.html',{'question_type_form': question_type_form})

@login_required
def questiontype_list(request):
    list = QuestionType.objects.all()
    questiontype_list = sorted(list, key = lambda QuestionType:QuestionType.questiontype_id)
    return render(request, 'administration/questiontype_list.html',{'questiontype_list': questiontype_list})

@login_required
def questiontype_edit(request, id):

    questiontype_list = QuestionType.objects.filter(pk=id).first()

    if request.method == 'POST':
        questiontype_list.questiontype_name = request.POST["questiontype_name"]
        questiontype_list.questiontype_description = request.POST["questiontype_description"]
        questiontype_list.created_by = User.objects.get(id = request.user.id)
        questiontype_list.save()
        return HttpResponseRedirect(reverse('questiontype_list'))

    else:
        questiontype_edit_form = QuestionTypeForm(instance=questiontype_list)
        return render(request, 'administration/questiontype_edit.html', {'questiontype_edit_form': questiontype_edit_form})