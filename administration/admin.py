from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Role)
admin.site.register(Customuser)
admin.site.register(Test)
admin.site.register(Testsection)
admin.site.register(SectionMapping)
admin.site.register(TestMapping)
admin.site.register(Complexity)
admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(QuestionChoice)
