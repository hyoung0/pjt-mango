# Generated by Django 3.2.18 on 2023-05-03 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0007_store_hits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='hits',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
