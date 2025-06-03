# face_app/models.py
from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    face_image = models.ImageField(upload_to='dataset/user_images/')

    def __str__(self):
        return self.username
