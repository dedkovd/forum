from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import detail_route, api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
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

class PostsViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostsSerializer

class CategoriesViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

	@detail_route(methods=['get', 'post'])
	def posts(self, request, pk):
		if request.method == 'POST':
			data = JSONParser().parse(request)
			data['category'] = pk
			data['is_reviewed'] = 'false'
			serializer = PostsSerializer(data = data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status = 400)

		if request.method == 'GET':
			posts = Post.objects.filter(category = self.get_object())

			serializer = PostsSerializer(posts, many=True)
			return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
	serializer = CustomUserSerializer(data = request.data)
	if serializer.is_valid():
		u = CustomUser.objects.create_user(
				serializer.data['username'],
				serializer.data['email'],
				serializer.data['password'],
				city = City.objects.get(pk=serializer.data['city'])
				)
		u.city = City.objects.get(pk=serializer.data['city'])
		u.save()
		return Response(serializer.data)
	else:
		return Response(serializer.errors, status = 400)
