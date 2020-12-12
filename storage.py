from util import create_dirs
import pickle
import re


class Storage(object):
    def __init__(self, app):
        self.app = app
        self.nodes = None

    def save(self):
        create_dirs(self.app.cfg['general']['storage_file_path'])
        with open(self.app.cfg['general']['storage_file_path'], 'wb') as f:
            pickle.dump(self.nodes, f)

    def load(self):
        with open(self.app.cfg['general']['storage_file_path'], 'rb') as f:
            self.nodes = pickle.load(f)

    def import_nodes_from_file(self):
        self.nodes = []
        with open(self.app.cfg['general']['nodes_list_file'], encoding='utf-8') as f:
            for line in f.readlines():
                name, ip, port = [i.strip() for i in re.split(r'\t+', line)]
                new_node = {
                    'name': name,
                    'ip': ip,
                    'port': port,
                    'is_up': None,
                    'status_code': None,
                    'rsa_certificate_expiry_date': None,
                    'gost_certificate_expiry_date': None,
                }
                self.nodes.append(new_node)
