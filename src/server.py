#!/usr/bin/python

#
# Simple WSGI server to kick off signing server
#

import webob
import app
import logging

from wsgiref.simple_server import make_server

logging.basicConfig(level=logging.DEBUG)

httpd = make_server('', 8000, app.wsgiapp)
print "Serving HTTP on port 8000..."

# Respond to requests until process is killed
httpd.serve_forever()


