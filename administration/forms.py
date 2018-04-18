from django.forms import ModelForm
from django import forms
from administration.models import *


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

