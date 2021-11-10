from json import JSONDecoder
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models


def default_val():
    return list


class Asteroid(models.Model):
    body = models.JSONField(encoder=DjangoJSONEncoder, decoder=JSONDecoder, default=default_val, unique=True)


class Observatory(models.Model):
    id = models.CharField(primary_key=True, max_length=12, editable=False)


class Device(models.Model):
    id = models.CharField(primary_key=True, max_length=12, editable=False)
    device_resolution = models.CharField(max_length=20)
    observatory = models.ForeignKey(Observatory, on_delete=models.CASCADE, default=None)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Sighting(models.Model):
    asteroid = models.ForeignKey(Asteroid, on_delete=models.CASCADE)
    observatory = models.ForeignKey(Observatory, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    matrix = models.JSONField(encoder=DjangoJSONEncoder, decoder=JSONDecoder, default=default_val)
