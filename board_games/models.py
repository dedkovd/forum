from django.db import models
from django.contrib.auth.models import User, UserManager

class Category(models.Model):
    category_name = models.CharField(max_length=100)

class Post(models.Model):
    category = models.ForeignKey('Category')
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    text = models.TextField()
    is_starred = models.BooleanField()

class Image(models.Model):
    image_file = models.ImageField(upload_to = 'images/')
    post = models.ForeignKey('Post')

class Country(models.Model):
    internal_id = models.IntegerField()
    name = models.CharField(max_length=50)

class City(models.Model):
    internal_id = models.IntegerField()
    country = models.ForeignKey('Country')
    name = models.CharField(max_length=50)

class CustomUser(User):
    city = models.ForeignKey('City')

    objects = UserManager()

