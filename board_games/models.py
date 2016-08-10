from django.db import models
from django.contrib.auth.models import User, UserManager

class Category(models.Model):
    category_name = models.CharField(max_length=100)

class Post(models.Model):
    category = models.ForeignKey('Category')
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, null = True, blank = True)
    text = models.TextField()
    is_reviewed = models.BooleanField(default = False)
    owner = models.ForeignKey('CustomUser')
    replie_to = models.ForeignKey('Post', null = True, blank = True)

class Image(models.Model):
    image_file = models.ImageField(upload_to = 'images/')
    post = models.ForeignKey('Post')

class Country(models.Model):
    internal_id = models.IntegerField()
    name = models.CharField(max_length=50)

class City(models.Model):
    internal_id = models.IntegerField()
    country = models.ForeignKey('Country', related_name='cities')
    name = models.CharField(max_length=50)

class CustomUser(User):
    city = models.ForeignKey('City')
    starred_posts = models.ManyToManyField('Post', blank = True)

    objects = UserManager()
