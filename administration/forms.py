from django import forms
from django.forms import ModelForm
from administration.models import Testsection , Role,Customuser
from django.contrib.auth.models import User


class TestsectionForm(ModelForm):
    class Meta:
        model = Testsection
        fields = ['section_name', 'section_description']

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
    custom_userid = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'UserID'}))
    custom_roleid = forms.ChoiceField(choices=[(x.role_id, x.role_description) for x in role ],widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Customuser
        fields = ('custom_userid', 'custom_roleid')


