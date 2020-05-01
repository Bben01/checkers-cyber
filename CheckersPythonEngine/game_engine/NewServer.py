from gevent.pywsgi import WSGIServer

from game_engine.FlaskServer import app

http_server = WSGIServer(('127.0.0.1', 5000), app)
http_server.stop_timeout = 20
http_server.serve_forever()
