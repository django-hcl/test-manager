from django.contrib import admin

# Register your models here.
from .models import Role, Customuser, Test, Testsection

admin.site.register(Role)
admin.site.register(Customuser)
admin.site.register(Test)
admin.site.register(Testsection)