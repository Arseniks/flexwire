# Generated by Django 3.2.17 on 2023-04-16 18:38

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('teams', '0003_auto_20230416_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='description',
            field=ckeditor.fields.RichTextField(
                help_text='Write description of your project',
                verbose_name='description',
            ),
        ),
    ]
