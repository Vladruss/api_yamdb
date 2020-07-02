#from django.contrib.auth import get_user_model
from django.db import models

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


