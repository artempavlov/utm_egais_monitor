from api import API
from web_server import WebServer
import time
from pebble import ThreadPool
import re


DAYS_BEFORE_EXPIRING = 14
REFRESH_DELAY_SECONDS = 300


class Node(API):
    def __init__(self, *args, name='', **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    @property
    def is_expiring(self):
        return self.rsa_certificate_time_left.days < DAYS_BEFORE_EXPIRING or self.gost_certificate_time_left.days < DAYS_BEFORE_EXPIRING


class Monitor(object):
    def __init__(self):
        self.web_app = WebServer(self)
        self.nodes = []
        self.nodes_down = []
        self.nodes_expiring = []
        self.load_nodes()

    def load_nodes(self):
        with open('nodes.txt', encoding='utf-8') as f:
            for line in f.readlines():
                name, ip, port = re.split(r'\t+', line)
                self.nodes.append(Node(ip, port, name=name))

    def run(self):
        self.web_app.run()
        while True:
            pool = ThreadPool(max_workers=200)
            for node in self.nodes:
                pool.schedule(node.update)
            pool.close()
            pool.join()
            nodes_down_new = []
            nodes_expiring_new = []
            for node in self.nodes:
                if node.is_up:
                    if node.is_expiring:
                        nodes_expiring_new.append(node)
                else:
                    nodes_down_new.append(node)
            self.nodes_down = nodes_down_new
            self.nodes_expiring = nodes_expiring_new
            time.sleep(REFRESH_DELAY_SECONDS)
