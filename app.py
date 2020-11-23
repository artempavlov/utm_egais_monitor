from api import API
import time
from pebble import ThreadPool, concurrent
from prometheus_client import start_http_server, Info, Gauge


class Server(object):
    def __init__(self, ip, port):
        self.api = API(ip, port)
        self.up = Gauge(('up' + ip + ':' + port).replace('.', '_').replace(':', '_'), 'Up')
        #self.up = Gauge('asdf', 'Up')

    def update(self):
        self.api.update()
        self.up.set(int(self.api.up))


class Monitor(object):
    def __init__(self):
        self.servers = []
        addresses = self.load_addresses()
        for address in addresses:
            self.servers.append(Server(address[0], address[1]))

    def load_addresses(self):
        with open('addresses.txt') as f:
            addresses = [elem.strip().split(':') for elem in f.readlines()]
        return addresses

    def run(self):
        self.run_prometheus_server()
        while True:
            pool = ThreadPool(max_workers=100)
            status = []
            for server in self.servers:
                pool.schedule(server.update)
            pool.close()
            pool.join()
            for server in self.servers:
                if server.up:
                    status.append([server.api.ip+':'+server.api.port, server.up, server.api.rsa_certificate_expiry_date])
                else:
                    status.append([server.api.ip+':'+server.api.port, server.api.up])
                print(server.api.ip+':'+server.api.port, server.api.up, server.api.rsa_certificate_expiry_date)
            print(status)
            time.sleep(30)

    @concurrent.thread
    def run_prometheus_server(self):
        start_http_server(38000)


if __name__ == '__main__':
    Monitor().run()