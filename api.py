from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import datetime


class API(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.last_checked = None
        self.is_up = False
        self.status_code = None
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

    def update(self):
        try:
            r = requests.get('http://'+self.ip+':'+self.port)
            self.status_code = r.status_code
            if r.status_code == 200:
                bs = BeautifulSoup(r.text, features="lxml")
                self.rsa_certificate_expiry_date = parse(bs.find(string='Сертификат RSA').findNext('div').contents[0].split(' по ')[1])
                self.gost_certificate_expiry_date = parse(bs.find(string='Сертификат ГОСТ').findNext('div').contents[0].split(' по ')[1])
                self.is_up = True
                return True
            else:
                self.is_up = False
                return False
        except:
            self.is_up = False
            return False
