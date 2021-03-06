# -*- coding: utf-8 -*-
'''
Модуль с описанием представлений

Данный модуль практически полностью зависит от django-restframework
(для реализации REST)
'''
from django.db.models import Q
from rest_framework import viewsets, permissions
from rest_framework.decorators import * 
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from board_games.models import *
from board_games.serializers import *

class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
	'''
	Представление перечня пользователей
	'''
	authentication_classes = (SessionAuthentication, TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = CustomUser.objects.all()
	serializer_class = CustomUserSerializer

class CountryViewSet(viewsets.ReadOnlyModelViewSet):
	'''
	Представление перечня стран
	'''
	queryset = Country.objects.all()
	serializer_class = CountrySerializer

	@detail_route()
    	def cities(self, request, pk):
		'''
		Детализация страны до городов
		'''
		cities = City.objects.filter(country = self.get_object())
		
		serializer = self.get_serializer(cities, many=True)
		return Response(serializer.data)

class IsAdminOrReadOnly(permissions.BasePermission):
	'''
	Дополнительный класс проверки прав - читать могут все,
	редактировать тольо админ
	'''
	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True

		return request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):
	'''
	Дополнительный класс для проверки прав - читать могут все,
	редактировать только владелец объекта
	'''
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.owner.id == request.user.id

class PostsViewSet(viewsets.ModelViewSet):
	'''
	Представление постов
	'''
	authentication_classes = (SessionAuthentication, TokenAuthentication,)
	permission_classes = (IsOwnerOrReadOnly,)
	serializer_class = PostsSerializer

	def get_queryset(self):
		'''
		Запрос отображает в зависимости от статуса пользователя
		или все посты или только посты пользователя + заапрувленные
		админом
		'''
		is_staff = self.request.user.is_staff
		if is_staff:
			return Post.objects.all()
		else:
			return Post.objects.filter(Q(is_reviewed = True) | 
						   Q(owner = self.request.user))

	def update(self, request, pk):
		'''
		Проверка что пользователь является владельцем поста или 
		админом при редактировании
		'''
		post = Post.objects.get(pk = pk)
		if not IsOwnerOrReadOnly().has_object_permission(request,self, post) and not request.user.is_staff:
			return Response(status = 401)
		data = JSONParser().parse(request)
		serializer = PostsSerializer(post, data=data, partial = True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		else:
			return Response(serializer.errors, status = 400)

	@detail_route(methods=['post','delete'])
	def starred(self, request, pk):
		'''
		Детализация к постам, добавленным в избранное
		(для добавления или удаления поста)
		'''
		if request.method == 'POST':
			request.user.customuser.starred_posts.add(pk)

		if request.method == 'DELETE':
			request.user.customuser.starred_posts.remove(pk)

		return Response(status = 200)

	@detail_route(methods=['get', 'post',],)
	@parser_classes((FormParser, MultiPartParser,))
	def images(self, request, pk):
		'''
		Детализация к изображениям поста
		'''
		post = Post.objects.get(pk = pk)
		if not IsOwnerOrReadOnly().has_object_permission(request,self, post):
			return Response(status = 401)
		if request.method == 'POST':
			request.data['parent_post'] = pk	
			serializer = ImageSerializer(data = request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status = 400)

		if request.method == 'GET':
			images = Image.objects.filter(parent_post = pk)
			serializer = ImageSerializer(images, many = True)
			return Response(serializer.data)

class CategoriesViewSet(viewsets.ModelViewSet):
	'''
	Представление категорий
	'''
	authentication_classes = (SessionAuthentication, TokenAuthentication,)
	permission_classes = (IsAuthenticated,IsAdminOrReadOnly,)
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

	@detail_route(methods=['get', 'post'], permission_classes=[IsAuthenticated,])
	def posts(self, request, pk):
		'''
		Детализация к постам категории
		'''
		if request.method == 'POST':
			data = JSONParser().parse(request)
			data['category'] = pk
			data['is_reviewed'] = 'false'
			data['owner'] = request.user.id
			serializer = PostsSerializer(data = data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			else:
				return Response(serializer.errors, status = 400)

		if request.method == 'GET':
			posts = Post.objects.filter(category = self.get_object())
			is_staff = request.user.is_staff
			if not is_staff:
				posts = posts.filter(Q(is_reviewed = True) |
						     Q(owner = request.user))

			serializer = PostsSerializer(posts, many=True)
			return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication,])
def starred_posts(request):
	'''
	Перечень избранных постов для текущего пользователя
	'''
	posts = request.user.customuser.starred_posts
	print posts

	serializer = PostsSerializer(posts, many=True)
	return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAdminUser,])
def ban_user(request,pk):
	'''
	Забанить пользователя
	'''
	u = CustomUser.objects.get(pk = pk)
	u.is_active = False
	u.save()
	return Response(status = 200)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAdminUser,])
def unban_user(request,pk):
	'''
	Снять бан с пользователя
	'''
	u = CustomUser.objects.get(pk = pk)
	u.is_active = True
	u.save()
	return Response(status = 200)

@api_view(['POST'])
def create_user(request):
	'''
	Зарегистрировать пользователя
	'''
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

