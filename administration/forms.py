from django.forms import ModelForm
from administration.models import Testsection


class TestsectionForm(ModelForm):
    class Meta:
        model = Testsection
        fields = ['section_name', 'section_description']