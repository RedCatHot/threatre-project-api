from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import Play
from theatre.tests.test_samples import sample_actor, sample_genre, sample_play, detail_url

PLAY_URL = reverse("theatre:play-list")
PERFORMANCE_URL = reverse("theatre:performance-list")


class AdminPlayApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com", "test_pass", is_staff=True
        )

        self.client.force_authenticate(self.user)

    def test_create_play(self):
        payload = {
            "title": "play 1",
            "description": "play 1 description",
        }

        res = self.client.post(PLAY_URL, payload)
        play = Play.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(play, key))

    def test_create_play_with_actor_and_genre(self):
        actor = sample_actor()
        genre = sample_genre()

        payload = {
            "title": "play 1",
            "description": "play 1 description",
            "genres": [genre.id],
            "actors": [actor.id],
        }

        res = self.client.post(PLAY_URL, payload)
        play = Play.objects.get(id=res.data["id"])

        actors = play.actors.all()
        genres = play.genres.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(actors.count(), 1)
        self.assertEqual(genres.count(), 1)

        self.assertIn(actor, actors)
        self.assertIn(genre, genres)

    def test_delete_not_allowed(self):
        play = sample_play()

        url = detail_url(play.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
