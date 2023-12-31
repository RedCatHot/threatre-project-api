# Generated by Django 4.1 on 2023-08-12 20:26

from django.db import migrations, models
import theatre.models


class Migration(migrations.Migration):
    dependencies = [
        ("theatre", "0003_alter_actor_options_alter_genre_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="play",
            name="image",
            field=models.ImageField(
                null=True, upload_to=theatre.models.movie_image_file_path
            ),
        ),
    ]
