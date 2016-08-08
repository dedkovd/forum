from rest_framework import serializers
from board_games.models import Country, City

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'id')
