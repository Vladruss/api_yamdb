from django.contrib.auth import get_user_model
from django.db import models
from _datetime import date

User = get_user_model()

class Genre(models.Model):
    name = models.CharField(max_length=25)
    slug = models.CharField(max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=25)
    slug = models.CharField(max_length=50)


class Title(models.Model):
    name = models.TextField(max_length=50)
    year = models.DateField(auto_now_add=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='category')
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING, related_name='genre')

    
class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="review"
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.text



class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.text
