from django.forms import ModelForm
from administration.models import Testsection,Test


class TestsectionForm(ModelForm):
    class Meta:
        model = Testsection
        fields = ['section_name', 'section_description']


class TestForm(ModelForm):
    class Meta:
        model = Test
        fields = ['test_name', 'test_description', 'test_duration_mins']