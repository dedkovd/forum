from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from board_games.models import *
from board_games.serializers import *

class CountryViewSet(viewsets.ModelViewSet):
	queryset = Country.objects.all()
	serializer_class = CountrySerializer

	@detail_route()
    	def cities(self, request, pk):
		cities = City.objects.filter(country = self.get_object())
		
		serializer = self.get_serializer(cities, many=True)
		return Response(serializer.data)
