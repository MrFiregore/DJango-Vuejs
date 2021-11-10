from rest_framework import serializers
from .models import *



class SightingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Sighting
        fields = '__all__'
        depth = 1


class AsteroidSerializer(serializers.ModelSerializer):
    body = serializers.SerializerMethodField('clean_json')
    id = serializers.IntegerField(read_only=True)
    sighting = serializers.SerializerMethodField('get_sighting')

    class Meta:
        model = Asteroid
        fields = '__all__'
        depth = 1

    def clean_json(self, obj):
        return obj.body

    def get_sighting(self, obj):
        return SightingSerializer(obj.sighting_set.defer("asteroid").all(), many=True).data
