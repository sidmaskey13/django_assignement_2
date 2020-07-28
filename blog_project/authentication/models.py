from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()

# Create your models here.
class UserDetail(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True)