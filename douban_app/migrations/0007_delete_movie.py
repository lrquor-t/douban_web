# Generated by Django 4.1.3 on 2023-03-15 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("douban_app", "0006_movie"),
    ]

    operations = [
        migrations.DeleteModel(name="Movie",),
    ]
