# Generated by Django 5.1.6 on 2025-02-19 10:02

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_category_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='defaults/user-icon.png', null=True, upload_to=blog.models.blogger_name_dict),
        ),
    ]
