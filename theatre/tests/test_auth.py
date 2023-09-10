from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import Play
from theatre.serializers import PlayListSerializer, PlayDetailSerializer
from theatre.tests.test_samples import sample_play, sample_genre, sample_actor, detail_url

PLAY_URL = reverse("theatre:play-list")
PERFORMANCE_URL = reverse("theatre:performance-list")


class UnauthenticatedCinemaTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLAY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCinemaTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "password"
        )

        self.client.force_authenticate(self.user)

    def test_list_plays(self):
        play1 = sample_play(title="play 1")
        play2 = sample_play(title="play 2")

        genre = sample_genre()

        actor1 = sample_actor()
        actor2 = sample_actor()

        play1.actors.add(actor1, actor2)
        play2.genres.add(genre)

        res = self.client.get(PLAY_URL)

        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_play_by_title_genre_actor(self):
        play1 = sample_play(title="play 1")
        play2 = sample_play()

        genre = sample_genre()

        actor = sample_actor()

        play1.genres.add(genre)
        play1.actors.add(actor)

        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)

        res = self.client.get(
            PLAY_URL,
            {
                "title": "play 1",
                "genres": f"{genre.id}",
                "actors": f"{actor.id}"
            },
        )

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_play_detail(self):
        play = sample_play()
        play.actors.add(sample_actor())
        play.genres.add(sample_genre())

        url = detail_url(play.id)
        res = self.client.get(url)

        serializer = PlayDetailSerializer(play)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_play_forbidden(self):
        payload = {
            "title": "play 1",
            "description": "play 1 description",
        }

        res = self.client.post(PLAY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
