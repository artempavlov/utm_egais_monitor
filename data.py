import api
import datetime
from pebble import ThreadPool


class Node(object):
    def __init__(self, app, index):
        self.app = app
        self.index = index

    @property
    def name(self):
        return self.storage_item['name']

    @property
    def ip(self):
        return self.storage_item['ip']

    @property
    def port(self):
        return self.storage_item['port']

    @property
    def address(self):
        return 'http://' + self.ip + ':' + self.port + '/'

    @property
    def is_up(self):
        return self.storage_item['is_up']

    @property
    def status_code(self):
        return self.storage_item['status_code']

    @property
    def rsa_certificate_expiry_date(self):
        return self.storage_item['rsa_certificate_expiry_date']

    @property
    def gost_certificate_expiry_date(self):
        return self.storage_item['gost_certificate_expiry_date']

    @property
    def rsa_certificate_time_left(self):
        return self.rsa_certificate_expiry_date - datetime.datetime.now(datetime.timezone.utc) \
            if self.rsa_certificate_expiry_date is not None else None

    @property
    def gost_certificate_time_left(self):
        return self.gost_certificate_expiry_date - datetime.datetime.now(datetime.timezone.utc) \
            if self.gost_certificate_expiry_date is not None else None

    @property
    def is_expiring(self):
        if self.rsa_certificate_time_left is None or self.gost_certificate_time_left is None:
            return None
        return self.rsa_certificate_time_left.days < self.app.cfg['general']['days_to_mark_expiring'] or \
            self.gost_certificate_time_left.days < self.app.cfg['general']['days_to_mark_expiring']

    @property
    def storage_item(self):
        return self.app.storage.nodes[self.index]

    def update(self):
        storage_item = self.storage_item
        status = api.get_status(self.ip, self.port)
        storage_item['is_up'] = status['is_up']
        storage_item['status_code'] = status['status_code']
        if status['rsa_certificate_expiry_date'] is not None:
            storage_item['rsa_certificate_expiry_date'] = status['rsa_certificate_expiry_date']
        if status['gost_certificate_expiry_date'] is not None:
            storage_item['gost_certificate_expiry_date'] = status['gost_certificate_expiry_date']


class Data(object):
    def __init__(self, app):
        self.app = app
        self.nodes = [Node(self.app, i) for i in range(len(self.app.storage.nodes))]

    @property
    def nodes_down(self):
        return [item for item in self.nodes if not item.is_up]

    @property
    def nodes_expiring(self):
        return [node for node in self.nodes if node.is_expiring]

    def update_nodes(self):
        pool = ThreadPool(max_workers=200)
        for node in self.nodes:
            pool.schedule(node.update)
        pool.close()
        pool.join()
