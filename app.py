from api import API
import time
from pebble import ThreadPool


class Monitor(object):
    def __init__(self):
        self.servers = []
        addresses = self.load_addresses()
        for address in addresses:
            self.servers.append(API(address[0], address[1]))

    def load_addresses(self):
        with open('addresses.txt') as f:
            addresses = [elem.strip().split(':') for elem in f.readlines()]
            #print(addresses)
        return addresses

    def run(self):

        #pool.
        while True:
            pool = ThreadPool(max_workers=100)
            status = []
            for server in self.servers:
                pool.schedule(server.update)
                #print(server)
                #server.update()
            pool.close()
            pool.join()
            for server in self.servers:
                if server.up:
                    status.append([server.ip+':'+server.port, server.up, server.rsa_certificate_expiry_date])
                else:
                    status.append([server.ip+':'+server.port, server.up])
                print(server.ip+':'+server.port, server.up, server.rsa_certificate_expiry_date)
            print(status)
            time.sleep(5)


if __name__ == '__main__':
    Monitor().run()