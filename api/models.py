from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(('email address'), unique=True)
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    User_role = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]
    role = models.CharField(max_length=25, choices=User_role, default=USER)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


"""
class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=25)
    description	 = models.TextField(blank=True)
    email = models.EmailField(max_length=25, unique=True)
    USER = 'u'
    ADMIN = 'a'
    MODERATOR = 'm'
    User_role = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]
    role = models.CharField(max_length=25, choices=User_role, default=USER)
    def __str__(self):
        return self.username
    USERNAME_FIELD = 'email'

"""
