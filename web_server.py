from flask import Flask, render_template
from pebble import concurrent


class WebServer():
    def __init__(self, app):
        self.app = app
        self.web_app = Flask('UTM EGAIS Monitor')
        self.web_app.route('/', methods=['GET'])(self.index)
        self.web_app.route('/down', methods=['GET'])(self.down)

    @concurrent.thread
    def run(self):
        self.web_app.run()

    def index(self):
        nodes_data = []
        for node in self.app.nodes:
            nodes_data.append(self.get_node_info(node))
        return render_template('index.html', nodes=nodes_data)

    def down(self):
        nodes_data = []
        for node in self.app.nodes_down:
            nodes_data.append(self.get_node_info(node))
        return render_template('down.html', nodes=nodes_data)


    def get_node_info(self, node):
        if not node.up:
            status = 'down'
        elif node.rsa_certificate_time_left.days < 14 or node.gost_certificate_time_left.days < 14:
            status = 'warning'
        else:
            status = 'up'
        #status_code = node.status_code if node.status_code is not None else 'Не отвечает'
        return {'address': node.name,
                'name': node.name,
                'status': status,
                'status_code': node.status_code,
                'rsa_certificate_expiry_date':
                    node.rsa_certificate_expiry_date.strftime("%d.%m.%Y, %H:%M:%S") if node.rsa_certificate_time_left is not None else '---',
                'gost_certificate_expiry_date':
                    node.gost_certificate_expiry_date.strftime("%d.%m.%Y, %H:%M:%S") if node.gost_certificate_time_left is not None else '---',}
