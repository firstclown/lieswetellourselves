#!/usr/bin/env python2.5
import sys, os

sys.path += ['django_src']
sys.path += ['django']

from fcgi import WSGIServer
from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'lieswetellourselves.settings'
WSGIServer(WSGIHandler()).run()
