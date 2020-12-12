import time


class Controller(object):
    def __init__(self, app):
        self.app = app

    def run(self):
        while True:
            self.app.data.update_nodes()
            self.app.storage.save()
            time.sleep(self.app.cfg['general']['refresh_delay_seconds'])
