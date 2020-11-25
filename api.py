from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime


class API(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.last_checked = None
        self.up = True
        self.rsa_certificate_good = None
        self.rsa_certificate_expiry_date = None
        self.gost_certificate_good = None
        self.gost_certificate_expiry_date = None

    @property
    def rsa_certificate_time_left(self):
        return self.rsa_certificate_expiry_date - datetime.datetime.now(datetime.timezone.utc) if self.rsa_certificate_expiry_date is not None else None

    @property
    def gost_certificate_time_left(self):
        return self.gost_certificate_expiry_date - datetime.datetime.now(datetime.timezone.utc) if self.gost_certificate_expiry_date is not None else None

    @property
    def address(self):
        return self.ip + ':' + self.port

    @property
    def name(self):
        return self.address

    def update(self):
        try:
            r = requests.get('http://'+self.ip+':'+self.port)
            if r.status_code == 200:
                bs = BeautifulSoup(r.text, features="lxml")
                self.rsa_certificate_expiry_date = parse(bs.find(string='Сертификат RSA').findNext('div').contents[0].split(' по ')[1])
                self.gost_certificate_expiry_date = parse(bs.find(string='Сертификат ГОСТ').findNext('div').contents[0].split(' по ')[1])
                self.up = True
                return True
            else:
                self.up = False
                return False
        except:
            self.up = False
            return False
