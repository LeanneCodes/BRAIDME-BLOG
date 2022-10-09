# Generated by Django 3.2 on 2022-10-09 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_remove_post_featured_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='featured_image_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
    ]
