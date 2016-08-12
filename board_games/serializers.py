# -*- coding: utf-8 -*-
'''
Модуль с описанием сериализаторов для объектов

Данный модуль зависит от пакета django-restframework
'''

from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from board_games.models import Country, Category, Post, CustomUser, Image

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    '''
    Сериализатор для стран
    '''
    class Meta:
        model = Country
        fields = ('name', 'id',)

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    '''
    Сериализатор для категорий
    '''
    class Meta:
        model = Category
        fields = ('category_name','id',)

class PostsSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для постов
    '''
    replies = serializers.ListField(child = RecursiveField(), read_only = True)
    class Meta:
        model = Post
        fields = (
                  'category', 
                  'title', 
                  'subtitle', 
                  'text', 
                  'is_reviewed', 
                  'owner', 
                  'id', 
                  'reply_to',
                  'replies',
                  )

class ImageSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для изображений
    '''
    class Meta:
        model = Image
        fields = ('image_file', 'parent_post')

class CustomUserSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для кастомного пользователя
    '''
    starred_posts = PostsSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'starred_posts', 'city', 'email', 'password')
