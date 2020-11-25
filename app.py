from api import API
from web_server import WebServer
import time
from pebble import ThreadPool, concurrent
from prometheus_client import start_http_server, Info, Gauge


class Metrics(object):
    def __init__(self):
        self.is_up = Gauge('is_up', 'status for each node', ['node'])
        self.down_list = Info('down_list', 'list of unavailable nodes')

    def set_is_up(self, ip, port, is_up):
        self.is_up.labels(node=('up' + ip + ':' + port).replace('.', '_')).set(int(is_up))

    # def reset_down_list(self):
    #     self.down_list.set().info({})
    #     self.down_list.

    def set_down_list(self, addresses):
        self.down_list.info({'Down': '\n'.join(addresses)})


class Monitor(object):
    def __init__(self):
        self.nodes = []
        #self.metrics = Metrics()
        self.web_app = WebServer(self)
        self.nodes_down = []
        addresses = self.load_addresses()
        for address in addresses:
            self.nodes.append(API(address[0], address[1]))

    def load_addresses(self):
        with open('addresses.txt') as f:
            addresses = [elem.strip().split(':') for elem in f.readlines()]
        return addresses

    def run(self):
        #self.run_prometheus_node()
        self.web_app.run()
        while True:
            pool = ThreadPool(max_workers=100)
            for node in self.nodes:
                pool.schedule(node.update)
            pool.close()
            pool.join()
            nodes_down_new = []
            for node in self.nodes:
                #self.metrics.set_is_up(node.ip, node.port, node.up)
                if not node.up:
                    #nodes_down.append(node.ip + ':' + node.port)
                    nodes_down_new.append(node)
            #self.metrics.set_down_list(nodes_down)
            self.nodes_down = nodes_down_new
            time.sleep(300)

    @concurrent.thread
    def run_prometheus_node(self):
        start_http_server(38000)


