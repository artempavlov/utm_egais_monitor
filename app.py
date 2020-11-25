from api import API
import time
from pebble import ThreadPool, concurrent
from prometheus_client import start_http_server, Info, Gauge


# class Node(object):
#     def __init__(self, ip, port):
#         self.api = API(ip, port)
#         #self.up = Gauge(('up' + ip + ':' + port).replace('.', '_'), 'Up')
#         #c.labels('get', '/')
#
#     def update(self):
#         self.api.update()
#         self.up.set(int(self.api.up))
# class DownList(object):
#     def __init__(self):
#         self.down_list = []
#         self.info = Info('down_list', 'list of unavailable nodes')
#
#     def reset(self):
#         self.down_list


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
        self.metrics = Metrics()
        addresses = self.load_addresses()
        for address in addresses:
            self.nodes.append(API(address[0], address[1]))

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
            nodes_down = []
            for node in self.nodes:
                self.metrics.set_is_up(node.ip, node.port, node.up)
                if not node.up:
                    nodes_down.append(node.ip + ':' + node.port)
                #if node.up:
                    #status.append([node.api.ip+':'+node.api.port, node.up, node.api.rsa_certificate_expiry_date])
                #else:
                    #status.append([node.api.ip+':'+node.api.port, node.api.up])
                #print(node.api.ip+':'+node.api.port, node.api.up, node.api.rsa_certificate_expiry_date)
            #print(status)
            self.metrics.set_down_list(nodes_down)
            time.sleep(5)

    @concurrent.thread
    def run_prometheus_node(self):
        start_http_server(38000)


if __name__ == '__main__':
    Monitor().run()
