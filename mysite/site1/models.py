"""
This contains the essential fields and behaviours of 
the data you're strong. Define your SQL data position here 
and automatically derive from it 
"""
from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone 
from django.utils.encoding import python_2_unicode_compatible

class Student(models.Model): # inherit from models.Model
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    YEAR_IN_SCHOOL_CHOICES = (
        (FRESHMAN,  'Freshman'),
        (SOPHOMORE,  'Sophomore'),
        (JUNIOR,  'Junior'),
        (SENIOR,  'Senior'),
        )
    year_in_school = models.CharField(
        max_length = 2,
        choices = YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )
    def is_upperclass(self):
        return self.year_in_school in (self.JUNIOR, self.SENIOR)
     
class Question(models.Model):
    question_text = models.CharField(max_length=200) 
    pub_date = models.DateTimeField('date published')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.question_text # When writing the class Question, it will return the question_text 
    
class Choice(models.Model):
    # ... Comments 
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text  # When writing the class Question, it will return the choice_text  


#class Topics(models.Model):
#    # ... Comments 
#    Physics = 'Physics'
#    Chemistry = 'Chemistry'
#    Biology = 'Biology'
#    Maths = 'Maths'

