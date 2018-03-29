from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_description = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.role_description)

class Customuser(models.Model):
    custom_userid = models.OneToOneField(User,on_delete=models.CASCADE)
    custom_roleid = models.ForeignKey(Role, on_delete=models.CASCADE)
    custom_assignedtest = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.custom_userid)


class Test(models.Model):
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=500)
    test_description = models.CharField(max_length=500)
    test_createdby = models.ForeignKey(User, on_delete=models.CASCADE)
    test_createdon = models.DateTimeField()
    test_duration_mins = models.DurationField()
    test_sectionid = models.CharField(max_length=100,null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.test_name)

class Testsection(models.Model):
    section_id = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=500)
    section_createdby = models.ForeignKey(User, on_delete=models.CASCADE)
    section_createdon = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.section_name)