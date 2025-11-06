from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .choices import STRENGTHS, INTERESTS
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True)
    dp = models.ImageField(default='images/user-circle.svg', upload_to='images/', blank=True)
    dob = models.DateField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name']

    def __str__(self):
        return self.get_full_name()
        
class Discipline(models.Model):
    BRANCHES = [
        ('science', 'Science'),
        ('arts', 'Arts'),
        ('social science', 'Social Science'),
        ('mgt science', 'Mgt Science'),
    ]
    branch = models.CharField(max_length=100, choices=BRANCHES)

    def __str__(self):
        return f'{self.branch}'

class Career(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    subject_group = models.CharField(max_length=255)
    strength = models.CharField(max_length=100, choices=STRENGTHS)
    interest = models.CharField(max_length=100, choices=INTERESTS)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Assessment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, editable=False)
    favorite_subject = models.CharField(max_length=100)
    classified = models.ForeignKey(Discipline, related_name="faculty", on_delete=models.CASCADE, null=True, blank=True )
    strength = models.CharField(max_length=100, choices=STRENGTHS)
    interest = models.CharField(max_length=100, choices=INTERESTS)
    career = models.ManyToManyField(Career, related_name='assessment', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.favorite_subject}'




