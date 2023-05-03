# Generated by Django 3.2.18 on 2023-05-03 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20230430_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]