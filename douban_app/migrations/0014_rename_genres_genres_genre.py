# Generated by Django 4.1.3 on 2023-04-18 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("douban_app", "0013_genres"),
    ]

    operations = [
        migrations.RenameField(
            model_name="genres", old_name="genres", new_name="genre",
        ),
    ]
