from rest_framework import serializers
from board_games.models import Country, Category, Post, CustomUser, Image

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'id',)

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('category_name','id',)

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('category', 'title', 'subtitle', 'text', 'is_reviewed', 'owner', 'id', 'reply_to',)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image_file', 'parent_post')

class CustomUserSerializer(serializers.ModelSerializer):
    starred_posts = PostsSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'starred_posts', 'city', 'email', 'password')
