from django.shortcuts import render
from rest_framework import viewsets
from board_games.models import Country
from board_games.serializers import CountrySerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

