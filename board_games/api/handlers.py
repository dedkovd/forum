from piston.handler import BaseHandler
from board_games.models import Country

class CountryHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Country

    def read(self, request, internal_id=None):
        base = Country.objects

        return base.get(internal_id = internal_id) if internal_id else base.all()
