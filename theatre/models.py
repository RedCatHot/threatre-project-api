from django.db import models
from rest_framework.exceptions import ValidationError

from user.models import User


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reservation for {self.user}"


class Genre(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        ordering = ["last_name"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Play(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    class Meta:
        ordering = ["name"]

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    class Meta:
        ordering = ["show_time"]

    def __str__(self):
        return f"{self.play.title} - {self.show_time}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        ordering = ["performance"]
        unique_together = ("row", "seat", "performance")

    def clean(self):
        if not (1 <= self.seat <= self.performance.theatre_hall.seats_in_row):
            raise ValidationError(
                {
                    "seat": f"seat must be "
                    f"in available range: "
                    f"(1, {self.performance.theatre_hall.seats_in_row}), not "
                    f"{self.seat}"
                }
            )

    def __str__(self):
        return f"Ticket {self.row}-{self.seat} for {self.performance.play.title}"
