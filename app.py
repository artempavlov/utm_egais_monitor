from api import API
import time
from pebble import ThreadPool, concurrent
from prometheus_client import start_http_node, Info, Gauge


class Node(object):
    def __init__(self, ip, port):
        self.api = API(ip, port)
        self.up = Gauge(('up' + ip + ':' + port).replace('.', '_'), 'Up')

    def update(self):
        self.api.update()
        self.up.set(int(self.api.up))


class Monitor(object):
    def __init__(self):
        self.nodes = []
        addresses = self.load_addresses()
        for address in addresses:
            self.nodes.append(Node(address[0], address[1]))

    def load_addresses(self):
        with open('addresses.txt') as f:
            addresses = [elem.strip().split(':') for elem in f.readlines()]
        return addresses

    def run(self):
        self.run_prometheus_node()
        while True:
            pool = ThreadPool(max_workers=100)
            status = []
            for node in self.nodes:
                pool.schedule(node.update)
            pool.close()
            pool.join()
            for node in self.nodes:
                if node.up:
                    status.append([node.api.ip+':'+node.api.port, node.up, node.api.rsa_certificate_expiry_date])
                else:
                    status.append([node.api.ip+':'+node.api.port, node.api.up])
                print(node.api.ip+':'+node.api.port, node.api.up, node.api.rsa_certificate_expiry_date)
            print(status)
            time.sleep(5)

    @concurrent.thread
    def run_prometheus_node(self):
        start_http_node(38000)


if __name__ == '__main__':
    Monitor().run()
