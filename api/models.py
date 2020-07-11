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


class Genre(models.Model):
    name = models.CharField(max_length=25)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=25)
    slug = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    year = models.IntegerField(null=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='titles', null=True)
    genre = models.ManyToManyField(Genre, related_name='titles')
    description = models.TextField(max_length=50, null=True)
    rating = models.IntegerField(default=None, null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='review')
    
    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return self.text
