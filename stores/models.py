from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=20)
    like_users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='like_stores')
    

class Store_info(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    info = models.TextField()
    address = models.URLField(max_length=200, blank=True)
    open_hours = models.TimeField()
    closing_hours = models.TimeField()
    parking = models.URLField(max_length=200, blank=True)


class Store_image(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    image = ProcessedImageField(upload_to='stores',
                                processors=[ResizeToFill(100,100)],
                                format='jpg',
                                options={'quality': 80})
    
    
class Menu(models.Model):
    menu = models.CharField(max_length=50)
    price = models.DecimalField(blank=True, max_digits=18, decimal_places=0)


class Category(models.Model):
    stores = models.ManyToManyField(Store, related_name='categories')
    category = models.CharField(max_length=20)