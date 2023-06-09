from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager
import os

# Create your models here.   
class Store(models.Model):
    name = models.CharField(max_length=20)
    like_users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='like_stores')
    
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    
    address = models.CharField(max_length=50, blank=True, null=True)
    latitude=models.FloatField(blank=True, null=True)
    longitude=models.FloatField(blank=True, null=True)
    
    open_hours = models.TimeField(blank=True, null=True)
    closing_hours = models.TimeField(blank=True, null=True)

    hits = models.PositiveIntegerField(default=0)

    def store_image_path(instance, filename):
        return f'stores/{instance.name}/{filename}'
    
    thumbnail = ProcessedImageField(upload_to=store_image_path, blank=True,
                                processors=[ResizeToFill(350,350)],
                                format='JPEG',
                                options={'quality': 100})
    
    category = models.CharField(max_length=20)

    tags = TaggableManager(blank = True)

    def __str__(self):
        return self.name 
    
    def delete(self, *args, **kargs):
        if self.thumbnail:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.thumbnail.path))
            dir_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.thumbnail.name))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        super(Store, self).delete(*args, **kargs)

    # @property
    # def update_counter(self):
    #     self.hits = self.hits + 1
    #     self.save()
    
    
class Menu(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    menu = models.CharField(max_length=50)
    price = models.DecimalField(blank=True, max_digits=18, decimal_places=0)


class StoreImage(models.Model):
    store = models.ForeignKey(to=Store, on_delete=models.CASCADE)

    def store_image_path(instance, filename):
        return f'stores/{instance.store}/{filename}'

    image = ProcessedImageField(upload_to=store_image_path, blank=True,
                                processors=[ResizeToFill(350,350)],
                                format='JPEG',
                                options={'quality': 100})
    
    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
            dir_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.image.name))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        super(StoreImage, self).delete(*args, **kargs)