# Generated by Django 3.2.18 on 2023-05-02 07:21

from django.db import migrations
import imagekit.models.fields
import stores.models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_alter_store_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='image',
        ),
        migrations.AddField(
            model_name='store',
            name='thumbnail',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to=stores.models.Store.store_image_path),
        ),
        migrations.AlterField(
            model_name='storeimage',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to=stores.models.StoreImage.store_image_path),
        ),
    ]