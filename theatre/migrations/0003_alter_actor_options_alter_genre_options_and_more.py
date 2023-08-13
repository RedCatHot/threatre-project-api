# Generated by Django 4.1 on 2023-08-12 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("theatre", "0002_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="actor",
            options={"ordering": ["last_name"]},
        ),
        migrations.AlterModelOptions(
            name="genre",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="performance",
            options={"ordering": ["show_time"]},
        ),
        migrations.AlterModelOptions(
            name="play",
            options={"ordering": ["title"]},
        ),
        migrations.AlterModelOptions(
            name="reservation",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AlterModelOptions(
            name="theatrehall",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="ticket",
            options={"ordering": ["performance"]},
        ),
        migrations.AlterField(
            model_name="play",
            name="actors",
            field=models.ManyToManyField(related_name="plays", to="theatre.actor"),
        ),
        migrations.AlterField(
            model_name="play",
            name="genres",
            field=models.ManyToManyField(related_name="plays", to="theatre.genre"),
        ),
        migrations.AlterField(
            model_name="play",
            name="title",
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="performance",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="theatre.performance",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="reservation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="theatre.reservation",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("row", "seat", "performance")},
        ),
    ]