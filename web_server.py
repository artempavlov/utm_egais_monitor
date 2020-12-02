from flask import Flask, render_template
from pebble import concurrent


def plural_days(n):
    days = ['день', 'дня', 'дней']

    if n % 10 == 1 and n % 100 != 11:
        p = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        p = 1
    else:
        p = 2

    return str(n) + ' ' + days[p]


class WebServer(object):
    def __init__(self, app):
        self.app = app
        self.web_app = Flask('UTM EGAIS Monitor')
        self.web_app.route('/', methods=['GET'])(self.index)
        self.web_app.route('/down', methods=['GET'])(self.down)
        self.web_app.route('/expiring', methods=['GET'])(self.expiring)

    @concurrent.thread
    def run(self):
        self.web_app.run()

    def index(self):
        nodes_data = []
        for node in self.app.nodes:
            nodes_data.append(self.get_node_info(node))
        return render_template('index.html', nodes=nodes_data, active_page='index')

    def down(self):
        nodes_data = []
        for node in self.app.nodes_down:
            nodes_data.append(self.get_node_info(node))
        return render_template('down.html', nodes=nodes_data, active_page='down')

    def expiring(self):
        nodes_data = []
        for node in self.app.nodes_expiring:
            nodes_data.append(self.get_node_info(node))
        return render_template('expiring.html', nodes=nodes_data, active_page='expiring')

    def get_node_info(self, node):
        if not node.is_up:
            status = 'down'
        elif node.is_expiring:
            status = 'expiring'
        else:
            status = 'up'
        if node.rsa_certificate_time_left is not None:
            rsa_certificate_expiry_date = '{} ({})'.format(node.rsa_certificate_expiry_date.strftime("%d.%m.%Y, %H:%M:%S"),
                                                            plural_days(node.rsa_certificate_time_left.days))
        else:
            rsa_certificate_expiry_date = '---'
        if node.gost_certificate_time_left is not None:
            gost_certificate_expiry_date = '{} ({})'.format(node.gost_certificate_expiry_date.strftime("%d.%m.%Y, %H:%M:%S"),
                                                             plural_days(node.gost_certificate_time_left.days))
        else:
            gost_certificate_expiry_date = '---'
        return {
            'address': node.address,
            'name': node.name,
            'status': status,
            'status_code': node.status_code,
            'rsa_certificate_expiry_date': rsa_certificate_expiry_date,
            'gost_certificate_expiry_date': gost_certificate_expiry_date,
            }
