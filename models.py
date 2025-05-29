# face_app/models.py
from django.db import models
from django.utils.crypto import get_random_string
from django.utils import timezone

class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    face_image = models.ImageField(upload_to='dataset/user_images/')
    def generate_verification_code(self):
        self.verification_code = get_random_string(6, allowed_chars='0123456789')
        self.save()

    def __str__(self):
        return self.username

    def __str__(self):
        return self.username
class Attendance(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"