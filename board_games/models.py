# -*- coding: utf-8 -*-
'''
Модуль с описанием моделей проекта

Данный модуль зависит от пакета django-resized (для корректировки размера
изображения при превышении допустимых размеров)
'''

from django.db import models
from django.contrib.auth.models import User, UserManager
from django_resized import ResizedImageField

class Category(models.Model):
	'''
	Модель категорий
	'''
	category_name = models.CharField(max_length=100)

class Post(models.Model):
	'''
	Модель постов

	Связана с моделью категорий и рекурсивно с моделью постов
	для реализации возможности ответа на другой пост

	Также ссылается на кастомную модель пользователя, для определения
	принадлежности к пользователю
	'''
	category = models.ForeignKey('Category')
	title = models.CharField(max_length=100)
	subtitle = models.CharField(max_length=100, null = True, blank = True)
	text = models.TextField()
	is_reviewed = models.BooleanField(default = False)
	owner = models.ForeignKey('CustomUser')
	reply_to = models.ForeignKey('Post', null = True, blank = True)

	@property
	def replies(self):
		'''
		Возвращает queryset ответов на конкретный пост
		'''
		return Post.objects.filter(models.Q(reply_to = self) &
					   models.Q(is_reviewed = True))

class Image(models.Model):
	'''
	Модель прикрепленных изображений к постам

	Реализовано отдельной моделью чтобы была возможность
	прикрепить несколько изображений к одному посту
	'''
	image_file = ResizedImageField(upload_to = 'images/')
	parent_post = models.ForeignKey('Post')

class Country(models.Model):
	'''
	Модель стран
	'''
	internal_id = models.IntegerField()
	name = models.CharField(max_length=50)

class City(models.Model):
	'''
	Модель городов

	Имеется ссылка на модель стран
	'''
	internal_id = models.IntegerField()
	country = models.ForeignKey('Country', related_name='cities')
	name = models.CharField(max_length=50)

class CustomUser(User):
	'''
	Модель кастомного пользователя

	Необходима для связки пользователя с городом проживания,
	а также для добавления постов в избранное пользователю
	'''
	city = models.ForeignKey('City')
	starred_posts = models.ManyToManyField('Post', blank = True)

	objects = UserManager()
