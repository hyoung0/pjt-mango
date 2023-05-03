from django.db import models

from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.

class User(AbstractUser):
    followings = models.ManyToManyField('self', related_name='followers', symmetrical=False)
    image = ProcessedImageField(upload_to='users', blank=True,
                                    processors=[ResizeToFill(100,100)],
                                    format='JPEG',
                                    options={'quality': 80})
    address = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.CharField(max_length=20)