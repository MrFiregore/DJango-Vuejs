from rest_framework import routers
from .viewsets import *


router = routers.SimpleRouter()
router.register('asteroid', AsteroidViewSet)
router.register('sighting', SightingViewSet)

urlpatterns = router.urls
