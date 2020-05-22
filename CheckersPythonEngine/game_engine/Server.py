from gevent.pywsgi import WSGIServer

from game_engine.FlaskApp import app

http_server = WSGIServer(('127.0.0.1', 5000), app)
http_server.serve_forever()
