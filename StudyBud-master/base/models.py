
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models


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


# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     body = models.TextField()
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return self.body[0:50]


#this one working model

# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     body = models.TextField()
#     hashtags = models.CharField(max_length=500, blank=True)  # optional
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-updated', '-created']

#     def __str__(self):
#         return self.body[0:50]

#     def save(self, *args, **kwargs):
#         # Extract hashtags automatically on save
#         import re
#         self.hashtags = " ".join(re.findall(r"#\w+", self.body))
#         super().save(*args, **kwargs)


#this on is trying to work
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    hashtags = models.CharField(max_length=500, blank=True)  # stores hashtags as space-separated text

    # Add new fields
    image = models.ImageField(upload_to='message_images/', blank=True, null=True)
    pdf = models.FileField(upload_to='message_pdfs/', blank=True, null=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[:50]

    def hashtag_list(self):
        """Return list of hashtags"""
        return [tag.strip() for tag in self.hashtags.split() if tag.strip()]

    def save(self, *args, **kwargs):
        import re
        # auto-detect hashtags in body (if any)
        found = re.findall(r"#\w+", self.body)
        # merge with manually added ones (if any)
        unique_tags = list(set(found + self.hashtag_list()))
        self.hashtags = " ".join(unique_tags)
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     import re
    #     # auto-detect hashtags in body (with or without #)
    #     found = re.findall(r"#?\w+", self.body)  # matches both #unit1 and unit1
    #     # remove any leading '#' from each tag
    #     clean_tags = [tag.lstrip("#") for tag in found]
    #     # remove duplicates
    #     unique_tags = list(set(clean_tags))
    #     # store as space-separated plain words
    #     self.hashtags = " ".join(unique_tags)
    #     super().save(*args, **kwargs)

