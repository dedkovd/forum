from rest_framework import serializers
from board_games.models import Country, Category, Post, CustomUser

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
        fields = ('category', 'title', 'subtitle', 'text', 'is_reviewed', 'id')

class CustomUserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all(), default=None)
    starred_posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True, default=None)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'posts', 'starred_posts', 'city', 'email', 'password')
