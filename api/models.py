#from django.contrib.auth import get_user_model
from django.db import models
from datetime import date

#User = get_user_model()


class Users(models.Model):
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
    name = models.CharField(max_length=50)
    year = models.DateField(auto_now_add=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='category')
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING, related_name='genre')
    description = models.TextField(max_length=50, null=True, blank=True)