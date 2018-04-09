from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    modified_date = models.DateTimeField(auto_now=True,editable=False)
    created_by = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name='created_%(class)ss')
    modified_by = models.ForeignKey(User,null=True, on_delete=models.CASCADE, related_name='modified_%(class)ss')
    INACTIVE = 0
    ACTIVE = 1
    STATUS = (
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
    )
    is_active = models.IntegerField(default=1, choices=STATUS)

    class Meta:
        abstract = True

class Role(BaseModel):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100,null=True)
    role_description = models.CharField(max_length=250,null=True,blank=True)

    def __str__(self):
        return str(self.role_name)

class Customuser(BaseModel):
    custom_userid = models.OneToOneField(User,on_delete=models.CASCADE)
    custom_roleid = models.ForeignKey(Role, on_delete=models.CASCADE)
    

    def __str__(self):
        return '%s %s' % (self.custom_userid,self.custom_roleid)


class Test(BaseModel):
    test_id = models.AutoField(primary_key=True)
    test_name = models.CharField(max_length=500)
    test_description = models.CharField(max_length=500,null=True,blank=True)
    test_duration_mins = models.IntegerField(default=0)    
    

    def __str__(self):
        return '%s' % self.test_name

class Testsection(BaseModel):
    section_id = models.AutoField(primary_key=True)
    section_name = models.CharField(max_length=500)
    section_description = models.CharField(max_length=500,null=True,blank=True)
    section_createdby = models.ForeignKey(User, on_delete=models.CASCADE)     

    def __str__(self):
        return str(self.section_name)

class SectionMapping(BaseModel):
    sectionmap_id = models.AutoField(primary_key=True)
    sectionmap_testid =  models.ForeignKey(Test, on_delete=models.CASCADE)
    sectionmap_userid =  models.ForeignKey(Testsection, on_delete=models.CASCADE)  
    

class TestMapping(BaseModel):
    testmap_id = models.AutoField(primary_key=True)
    testmap_testid =  models.ForeignKey(Test, on_delete=models.CASCADE)
    testmap_userid =  models.ForeignKey(User, on_delete=models.CASCADE)   


class Complexity(BaseModel):
    complex_id = models.AutoField(primary_key=True)
    complex_name =  models.ForeignKey(Test, on_delete=models.CASCADE)
    complex_description = models.CharField(max_length=500,null=True,blank=True)
 
    

class QuestionType(BaseModel):
    questiontype_id = models.AutoField(primary_key=True)
    questiontype_name = models.CharField(max_length=250)
    questiontype_description = models.CharField(max_length=500,null=True,blank=True)


class Question(BaseModel):
    question_id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=1000)
    question_complex = models.ForeignKey(Complexity, on_delete=models.CASCADE)
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    question_section = models.ForeignKey(Testsection, on_delete=models.CASCADE)
    
    

class QuestionChoice(BaseModel):
    choice_id = models.AutoField(primary_key=True)
    choice_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=500)
    choice_is_correct = models.BooleanField()
    
    

    