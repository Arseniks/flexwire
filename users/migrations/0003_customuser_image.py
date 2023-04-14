# Generated by Django 3.2.17 on 2023-04-14 13:00

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_auto_20230412_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='user_avatars/',
                verbose_name='avatar',
            ),
        ),
    ]
