# Generated by Django 3.2.18 on 2023-04-30 15:54

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_review_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='like_users',
        ),
        migrations.AlterField(
            model_name='review',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='reviews_image_path'),
        ),
    ]
