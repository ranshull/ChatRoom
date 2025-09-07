from django.contrib.auth.models import User, Group
from django.db import models
from django import forms
# from .models import UserProfile

class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message by {self.sender} in {self.group.name} at {self.timestamp}'

class PDFFile(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='pdf_files')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='pdfs/')
    hashtag = models.CharField(max_length=50, blank=True)  # new field
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'PDF in {self.group.name} uploaded by {self.uploaded_by}'

class Doubt(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='doubts')
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    hashtag = models.CharField(max_length=50, blank=True)  # new field
    is_resolved = models.BooleanField(default=False)
    asked_at = models.DateTimeField(auto_now_add=True)



class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES)
    college_id = models.CharField(max_length=50)



# Create your models here.
