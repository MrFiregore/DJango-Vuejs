import pytest
from apps.asteroid import Asteroid
# from tests.factories import UsuarioAdminFactory, UsuarioComunFactory


@pytest.mark.django_db
def test_list_asteroids(client):
    asteroid = Asteroid.objects.all()
    all_asteroids = list(asteroid)
    asteroids = client.get('/api/asteroid')
    i = 2