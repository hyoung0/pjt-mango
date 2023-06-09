# Generated by Django 3.2.18 on 2023-05-02 05:13

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import reviews.models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20230502_0326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='image',
        ),
        migrations.CreateModel(
            name='ReviewImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=reviews.models.ReviewImage.review_image_path)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.review')),
            ],
        ),
    ]
