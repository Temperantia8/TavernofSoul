import imp
import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

wsgi = imp.load_source('wsgi', '../passenger_wsgi_ktest.py')
application = wsgi.application
