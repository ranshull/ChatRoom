
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from .supabase_storage import upload_file  # import your Supabase helper
import re
from django.contrib.auth.models import BaseUserManager



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        # Auto-generate a username if it doesn't exist
        if 'username' not in extra_fields or not extra_fields['username']:
            extra_fields['username'] = email.split('@')[0] + str(self.model.objects.count())
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager() 


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name



#this on is  working :)
# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     body = models.TextField()
#     hashtags = models.CharField(max_length=500, blank=True)  # stores hashtags as space-separated text

#     # Add new fields
#     image = models.ImageField(upload_to='message_images/', blank=True, null=True)
#     pdf = models.FileField(upload_to='message_pdfs/', blank=True, null=True)

#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return self.body[:50]

#     def hashtag_list(self):
#         """Return list of hashtags"""
#         return [tag.strip() for tag in self.hashtags.split() if tag.strip()]

#     def save(self, *args, **kwargs):
#         import re
#         # auto-detect hashtags in body (if any)
#         found = re.findall(r"#\w+", self.body)
#         # merge with manually added ones (if any)
#         unique_tags = list(set(found + self.hashtag_list()))
#         self.hashtags = " ".join(unique_tags)
#         super().save(*args, **kwargs)



class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    body = models.TextField()
    hashtags = models.CharField(max_length=500, blank=True)

    # Temporarily store uploaded file, will be sent to Supabase
    image = models.ImageField(upload_to='temp/', blank=True, null=True)
    pdf = models.FileField(upload_to='temp/', blank=True, null=True)

    # Store permanent URLs
    image_url = models.URLField(blank=True, null=True)
    pdf_url = models.URLField(blank=True, null=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[:50]

    def hashtag_list(self):
        return [tag.strip() for tag in self.hashtags.split() if tag.strip()]

    def save(self, *args, **kwargs):
        # Handle hashtags
        found = re.findall(r"#\w+", self.body)
        unique_tags = list(set(found + self.hashtag_list()))
        self.hashtags = " ".join(unique_tags)

        # Save first to get file data from image/pdf
        super().save(*args, **kwargs)

        # Upload image to Supabase
        if self.image and not self.image_url:
            img_path = f"message_images/{self.id}_{self.image.name}"
            self.image_url = upload_file(self.image, img_path)

        # Upload PDF to Supabase with correct MIME type
        if self.pdf and not self.pdf_url:
            pdf_path = f"message_pdfs/{self.id}_{self.pdf.name}"
            self.pdf_url = upload_file(self.pdf, pdf_path)

        # Update URL fields without recursion
        if self.image_url or self.pdf_url:
            update_fields = ['hashtags']
            if self.image_url:
                update_fields.append('image_url')
            if self.pdf_url:
                update_fields.append('pdf_url')
            super().save(update_fields=update_fields)

# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey('Room', on_delete=models.CASCADE)
#     body = models.TextField()
#     hashtags = models.CharField(max_length=500, blank=True)

#     # Temporarily store uploaded file, will be sent to Supabase
#     image = models.ImageField(upload_to='temp/', blank=True, null=True)
#     pdf = models.FileField(upload_to='temp/', blank=True, null=True)

#     # Store permanent URLs
#     image_url = models.URLField(blank=True, null=True)
#     pdf_url = models.URLField(blank=True, null=True)

#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return self.body[:50]

#     def hashtag_list(self):
#         return [tag.strip() for tag in self.hashtags.split() if tag.strip()]

#     def save(self, *args, **kwargs):
#         # Handle hashtags
#         found = re.findall(r"#\w+", self.body)
#         unique_tags = list(set(found + self.hashtag_list()))
#         self.hashtags = " ".join(unique_tags)

#         # Save first to get file data from image/pdf
#         super().save(*args, **kwargs)

#         # Upload image to Supabase
#         if self.image and not self.image_url:
#             img_path = f"message_images/{self.image.name}"
#             self.image_url = upload_file(self.image, img_path)

#         # Upload PDF to Supabase
#         if self.pdf and not self.pdf_url:
#             pdf_path = f"message_pdfs/{self.pdf.name}"
#             self.pdf_url = upload_file(self.pdf, pdf_path)

#         # Update URL fields without recursion
#         super().save(update_fields=['image_url', 'pdf_url'])

# ---------------------------------------------------------------------------------------------------------------------

class Announcement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    venue = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.TimeField()
    school_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class EventInterest(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name="interests")
    roll_no = models.CharField(max_length=20)
    course = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.roll_no} - {self.announcement.title}"
