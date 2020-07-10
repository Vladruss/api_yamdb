#from django.contrib.auth import get_user_model
from django.db import models
from datetime import date

#User = get_user_model()


class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=25)
    description	 = models.TextField()
    email = models.EmailField(max_length=25)
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


class Genre(models.Model):
    name = models.CharField(max_length=25)
    slug = models.CharField(max_length=50, unique=True)


class Category(models.Model):
    name = models.CharField(max_length=25)
    slug = models.CharField(max_length=50, unique=True)


class Title(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    year = models.IntegerField(null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='titles', null=True)
    genre = models.ManyToManyField(Genre, related_name='genres')
    description = models.TextField(max_length=50, null=True)
    #rating = models.IntegerField(default=None)