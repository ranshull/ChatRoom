from django.contrib import admin
from .models import Message, PDFFile, Doubt

admin.site.register(Message)
admin.site.register(PDFFile)
admin.site.register(Doubt)
