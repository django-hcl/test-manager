from django import forms
from django.forms import ModelForm

from administration.models import Testsection, Role,Customuser, Question, QuestionType,Complexity, Test
from django.contrib.auth.models import User


class TestForm(ModelForm):
    test_name = forms.CharField(
        required=True,
        label='Test Name',
        max_length=15,
        widget=forms.TextInput(attrs={'class':'form-control input-sm'})
    )
    test_description = forms.CharField(
        required=True,
        label='Description',
        max_length=30,
        widget=forms.TextInput(attrs={'class':'form-control input-sm'}))

    class Meta:
        model = Test
        fields = ['test_name', 'test_description', 'test_duration_mins']


class TestsectionForm(ModelForm):
    section_name = forms.CharField(
        required=True,
        label='Section Name',
        max_length=15,
        widget=forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Enter Section Name'})
    )
    section_description = forms.CharField(
        required=True,
        label='Section Name',
        max_length=30,
        widget=forms.TextInput(attrs={'class':'form-control input-sm', 'placeholder':'Enter Section description'}))

    class Meta:
        model = Testsection
        fields = ['section_name', 'section_description']


    '''def clean(self):
        data = self.cleaned_data
        section_name = data['section_name']
        section_description = data['section_description']
        if section_name == "":
            print("entered validation")
            raise forms.ValidationError("plz give valid input")
        return data'''



class UserForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))

    class Meta:
        model = User
        fields = ('username','email')

    '''
    def clean_username(self):
        username = self.cleaned_data['username']
        if username == "":
            raise forms.ValidationError("Enter a username", code="username",)
        return username
    def clean_email(self):
        email = self.cleaned_data['username']
        if email is None:
            raise forms.ValidationError("Enter EmailID", code="email",)
        return email'''


class CustomUserForm(ModelForm):

    role = Role.objects.all()
    custom_userid = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'UserID','readonly':'readonly'}))
    custom_roleid = forms.ChoiceField(choices=[(x.role_id, x.role_description) for x in role ],widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Customuser
        fields = ('custom_userid', 'custom_roleid')


class QuestionAddForm(ModelForm):
    class Meta:
        model = Question
        fields = ('question_text','question_complex','question_type','question_section')

    def __init__(self, *args, **kwargs):
        super(QuestionAddForm, self).__init__(*args, **kwargs)
        self.testsection = Testsection.objects.all()
        question_section_choice = [(x.section_id, x.section_name) for x in self.testsection ]
        question_section_choice.insert(0,(0, '--- Select ---'))
        self.fields['question_section'] = forms.ChoiceField(
            choices=question_section_choice,widget=forms.Select(attrs={'class':'form-control'}))

    def addDefaultOption(options):
        return options.insert(0,(0, '--- Select ---'))

    complexity = Complexity.objects.all()
    questiontype = QuestionType.objects.all()

    question_type_choice = [(x.questiontype_id, x.questiontype_name) for x in questiontype ]
    addDefaultOption(question_type_choice)

    question_complex_choice = [(x.complex_id, x.complex_name) for x in complexity ]
    addDefaultOption(question_complex_choice)


    question_text = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Question Text'}))
    question_complex = forms.ChoiceField(choices=question_complex_choice,widget=forms.Select(attrs={'class':'form-control'}))
    question_type = forms.ChoiceField(choices=question_type_choice,widget=forms.Select(attrs={'class':'form-control'}))


class ComplexityForm(ModelForm):
    complex_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Complexity name'}))
    complex_description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Complexity description'}))

    class Meta:
        model = Complexity
        fields = ('complex_name','complex_description')


class QuestionTypeForm(ModelForm):
    questiontype_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Question Type'}))
    questiontype_description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Question Type description'}))

    class Meta:
        model = QuestionType
        fields = ('questiontype_name','questiontype_description')




