from rest_framework import serializers
from board_games.models import Country

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'internal_id')
