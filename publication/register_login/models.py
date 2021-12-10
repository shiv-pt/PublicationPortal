from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import EmailField
from django.contrib.auth.models import AbstractUser
from PIL import Image
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    # class Meta:
    #     db_table = 'registration'
