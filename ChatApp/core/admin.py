from django.contrib import admin
from .models import Message, PDFFile, Doubt, UserProfile

admin.site.register(Message)
admin.site.register(PDFFile)
admin.site.register(Doubt)
admin.site.register(UserProfile)