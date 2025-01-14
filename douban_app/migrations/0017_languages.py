# Generated by Django 4.1.3 on 2023-04-23 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("douban_app", "0016_subject"),
    ]

    operations = [
        migrations.CreateModel(
            name="Languages",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("movie_id", models.IntegerField(verbose_name="电影ID")),
                ("movie_name", models.CharField(max_length=110, verbose_name="电影名")),
                ("language", models.CharField(max_length=15, verbose_name="语种")),
            ],
            options={"verbose_name": "语种信息管理", "verbose_name_plural": "语种信息管理",},
        ),
    ]
