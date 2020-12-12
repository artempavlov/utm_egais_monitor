from config_manager import ConfigManager
from log_manager import LogManager
from storage import Storage
from data import Data
from controller import Controller
from web_server import WebServer


import sys


CONFIG_PATH = 'config.toml'


class App(object):
    def __init__(self):
        self.CONFIG_PATH = CONFIG_PATH
        self.config_manager = ConfigManager()
        self.config_manager.read_config(self.CONFIG_PATH)
        self.cfg = self.config_manager.cfg
        self.log_manager = LogManager(self.cfg['general']['log_path'])
        if self.cfg['general']['redirect_output']:
            sys.stdout = open(self.cfg['general']['redirect_output'], 'a')
        if self.cfg['general']['redirect_traceback']:
            sys.stderr = open(self.cfg['general']['redirect_traceback'], 'a')
        self.logging = self.log_manager.logging

        self.storage = Storage(self)
        if self.cfg['general']['import_nodes_from_file']:
            self.storage.import_nodes_from_file()
        else:
            self.storage.load()
        self.data = Data(self)
        self.web_app = WebServer(self)
        self.web_app.run()
        self.controller = Controller(self)
        self.controller.run()

