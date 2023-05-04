from django.db import models
from django.conf import settings
from stores.models import Store
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    emote_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='emote_reviews', through='Emote')
    content = models.CharField(max_length=500)
    rating = models.IntegerField()

    def rate_to_star(self):
        return '★' * self.rating
    
    def rate_to_empty_star(self):
        return '☆' * (5 - self.rating)
    
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at
        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(time.seconds // 60) + '분 전'
        elif time < timedelta(days=1):
            return str(time.seconds // 3600) + '시간 전'
        elif time < timedelta(weeks=1):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return self.created_at.strftime('%Y-%m-%d')
        
    updated_at = models.DateField(auto_now=True)


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def review_image_path(instance, filename):
        return f'reviews/{instance.review.user.username}/{filename}'

    image = ProcessedImageField(upload_to=review_image_path, blank=True, null=True,
                                processors=[ResizeToFill(100,100)],
                                format='JPEG',
                                options={'quality': 80})


class Emote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    emotion = models.CharField(max_length=10)