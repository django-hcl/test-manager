from django.forms import ModelForm
from django import forms
from administration.models import *


class TestsectionForm(ModelForm):
    class Meta:
        model = Testsection
        fields = ['section_name', 'section_description']

    def clean(self):
        data = self.cleaned_data
        section_name = data['section_name']
        section_description = data['section_description']
        if section_name == "":
            print("entered validation")
            raise forms.ValidationError("plz give valid input")
        return data


class TestForm(ModelForm):
    class Meta:
        model = Test
        fields = ['test_name', 'test_description', 'test_duration_mins']

