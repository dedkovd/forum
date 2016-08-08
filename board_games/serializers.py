from rest_framework import serializers
from board_games.models import Country

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    cities = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Country
        fields = ('name', 'internal_id', 'cities')
