"""forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from rest_framework.authtoken import views as av
from board_games import views

router = routers.DefaultRouter()
router.register(r'countries', views.CountryViewSet)
router.register(r'categories', views.CategoriesViewSet)
router.register(r'posts', views.PostsViewSet)
router.register(r'users', views.CustomUserViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', av.obtain_auth_token),
    url(r'^api/register/', views.create_user),
    url(r'^api/starred/', views.starred_posts),
    url(r'^api/ban/(?P<pk>\d)/', views.ban_user),
    url(r'^api/unban/(?P<pk>\d)/', views.unban_user),
]
