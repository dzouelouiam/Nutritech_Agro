from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model  # Import from django.contrib.auth
from django.db import models
from django.conf import settings
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, default="default_user")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

User = get_user_model()
class Form(models.Model):
    TOPIC_CHOICES = [
        ('Engrais solides', 'Engrais solides'),
        ('Engrais spéciaux hydrosolubles', 'Engrais spéciaux hydrosolubles'),
        ('Correcteurs de carence', 'Correcteurs de carence'),
        ('Biostimulants', 'Biostimulants'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Replace 1 with the ID of a real user
    email = models.EmailField()
    region = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.topic} by {self.user.username}"
    
class Comment(models.Model):
    form = models.ForeignKey(Form, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


