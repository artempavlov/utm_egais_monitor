from web_server import WebServer
from flask import Flask
#from flask_bootstrap import Bootstrap

app = Flask(__name__)

web_server = WebServer()
#WebServer.register(app, route_base='/')
app.route('/', methods=['GET'])(web_server.index)
app.route('/test', methods=['GET'])(web_server.test)
#Bootstrap(app)
app.run()