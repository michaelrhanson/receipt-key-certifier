#
# WSGI application to run signing server
#

import webob
import crypto
import base64
import logging

def wsgiapp(environ, start_response):
    req = webob.Request(environ) 

    try:

        result =crypto.sign(req.params["input"])
        start_response('200 OK', [('Content-Type', 'text/plain')])
        yield base64.b64encode(result)

    except Exception, e:

        logging.exception(e)
        start_response('500 Server error', [('Content-Type', 'text/plain')])
        yield "There was an error."

