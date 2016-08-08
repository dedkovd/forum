from django.conf.urls.defaults import *
from piston.resource import Resource
from forum.board_games.api.handlers import CountryHandler

country_handler = Resource(CountryHandler)

urlpatterns = patterns('',
        url(r'^country/(?P<internal_id>[^/]+/', country_handler),
        url(r'^countries/', country_handler),
        )
