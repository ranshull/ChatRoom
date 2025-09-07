from django import forms
from .models import Message, PDFFile, Doubt
from django import forms
from .models import UserProfile

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDFFile
        fields = ['file']

class DoubtForm(forms.ModelForm):
    class Meta:
        model = Doubt
        fields = ['question']



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_type', 'college_id']

