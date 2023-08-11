from rest_framework import serializers
from .models import TheatreHall, Genre, Actor, Play, Performance, Reservation, Ticket


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class PlaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = '__all__'


class PlayListSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name",
    )

    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors")


class PlayDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors")


class PerformanceSerializer(serializers.ModelSerializer):
    play = PlaySerializer()
    theatre_hall = TheatreHallSerializer()

    class Meta:
        model = Performance
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
