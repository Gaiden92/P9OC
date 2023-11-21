from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profil_photo = models.ImageField()

    def __unicode__(self):
        return self.username
    
