from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobilenumber = models.CharField(max_length=15)
    
class StudentInfo(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    math_marks_hs = models.IntegerField()
    science_marks_hs = models.IntegerField()
    english_marks_hs = models.IntegerField()
    hindi_marks_hs = models.IntegerField()
    hs_percentage = models.FloatField(blank=True, null=True)
    physics_marks_10p2 = models.IntegerField()
    chemistry_marks_10p2 = models.IntegerField()
    mathematics_marks_10p2 = models.IntegerField()
    marks_10p2_percentage = models.FloatField(blank=True, null=True)
    PREFERENCE_CHOICES = [
        ('computer_science_engineering', 'Computer Science and Engineering'),
        ('electronics_communication_engineering', 'Electronics and Communication Engineering'),
        ('information_technology', 'Information Technology'),
    ]
    
    preference_1 = models.CharField(max_length=50, choices=PREFERENCE_CHOICES, blank=True, null=True)
    preference_2 = models.CharField(max_length=50, choices=PREFERENCE_CHOICES, blank=True, null=True)
    preference_3 = models.CharField(max_length=50, choices=PREFERENCE_CHOICES, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.full_name
    
    
