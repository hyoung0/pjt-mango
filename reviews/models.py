from django.db import models
from django.conf import settings
from stores.models import Store
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
    emote_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='emote_reviews', through='Emote')
    content = models.CharField(max_length=500)
    rating = models.IntegerField()

    def reviews_image_path(instance, filename):
        return f'reviews/{instance.user.username}/{filename}'

    image = ProcessedImageField(upload_to='reviews_image_path', blank=True, null=True,
                                processors=[ResizeToFill(100,100)],
                                format='jpg',
                                options={'quality': 80})
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def rate_to_star(self):
        return '★' * self.rating


class Emote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    emotion = models.CharField(max_length=10)