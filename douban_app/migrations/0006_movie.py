# Generated by Django 4.1.3 on 2023-03-15 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("douban_app", "0005_delete_movie"),
    ]

    operations = [
        migrations.CreateModel(
            name="Movie",
            fields=[
                ("movie_id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
                ("alias", models.CharField(max_length=200)),
                ("actors", models.TextField()),
                ("cover", models.CharField(max_length=150)),
                ("directors", models.CharField(max_length=150)),
                ("genres", models.CharField(max_length=50)),
                ("regions", models.CharField(max_length=50)),
                ("languages", models.CharField(max_length=60)),
                ("release_year", models.CharField(max_length=4)),
                ("mins", models.CharField(max_length=15)),
                ("score", models.FloatField()),
                ("storyline", models.TextField()),
            ],
        ),
    ]