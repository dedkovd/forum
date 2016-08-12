#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Вспомогательный модуль для наполнения базы данными о странах
и городах

Работает достаточно медленно, но с учетом того, что запускается
один раз - оптимизация бессмысленна.
'''

import sys, os, csv
sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'forum.settings'
from django.conf import settings

from board_games.models import Country, City

print "Fill countries table"
with open('country.csv', 'rb') as c:
    r = csv.reader(c, delimiter=';', quotechar='"')
    next(r, None)
    for row in r:                                  
        x = Country(name = row[2], internal_id = row[0])
        x.save()

print "Fill cities table"
with open('city.csv', 'rb') as c:
    r = csv.reader(c, delimiter=';', quotechar='"')
    next(r, None)
    for row in r:
        country = Country.objects.get(internal_id=row[1])
        x = City(name = row[3], internal_id = row[0], country = country)
        x.save()
