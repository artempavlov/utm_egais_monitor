from flask import render_template
from flask_classy import FlaskView, route
from app import Monitor


class WebServer():
    def __init__(self):
        self.app = Monitor(self)
        self.app.run()

    #@route('/')
    def index(self):
        nodes_data = []
        for node in self.app.nodes:
            nodes_data.append(self.get_node_info(node))
        return render_template('index.html', nodes=nodes_data)

    #@route('/test')
    def test(self):
        return render_template('test.html')

    def get_node_info(self, node):
        if not node.up:
            status = 'down'
        elif node.rsa_certificate_time_left.days < 14 or node.gost_certificate_time_left.days < 14:
            status = 'warning'
        else:
            status = 'up'
        return {'address': node.name,
                'name': node.name,
                'status': status,
                'rsa_certificate_expiry_date':
                    node.rsa_certificate_expiry_date.strftime("%m.%d.%Y, %H:%M:%S") if node.rsa_certificate_time_left is not None else '---',
                'gost_certificate_expiry_date':
                    node.gost_certificate_expiry_date.strftime("%m.%d.%Y, %H:%M:%S") if node.gost_certificate_time_left is not None else '---',}

# @web_app.route('/')
# def index():
#     nodes_data = []
#     for node in app.app.nodes:
#         nodes_data.append({'address': node.name,
#                            'name': node.name,
#                             'status': node.up})
#     return render_template('index.html', nodes=nodes_data)