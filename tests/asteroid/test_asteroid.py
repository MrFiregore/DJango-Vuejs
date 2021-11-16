import pytest
from django.test import TestCase, Client
from apps.asteroid.models import Asteroid
# from tests.factories import UsuarioAdminFactory, UsuarioComunFactory


@pytest.mark.django_db
def test_list_asteroids(client):
    asteroid = Asteroid.objects.all()
    all_asteroids = list(asteroid)
    asteroids = client.get('/api/asteroid')
    i = 2