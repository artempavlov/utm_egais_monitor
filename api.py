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
        #self.data = {'Сертификат RSA': None, 'Сертификат ГОСТ': None}
        self.rsa_certificate_good = None
        self.rsa_certificate_expiry_date = None
        self.gost_certificate_good = None
        self.gost_certificate_expiry_date = None

    @property
    def rsa_certificate_time_left(self):
        return self.rsa_certificate_expiry_date - datetime.datetime.now() if self.rsa_certificate_expiry_date is not None else None

    @property
    def rsa_certificate_time_left(self):
        return self.gost_certificate_expiry_date - datetime.datetime.now() if self.gost_certificate_expiry_date is not None else None

    def update(self):
        try:
            r = requests.get('http://'+self.ip+':'+self.port)
            if r.status_code == 200:
                bs = BeautifulSoup(r.text, features="lxml")
                #with open('test.html', 'w', encoding='utf-8') as output_file:
                #    output_file.write(r.text)
                self.rsa_certificate_expiry_date = parse(bs.find(string='Сертификат RSA').findNext('div').contents[0].split(' по ')[1])
                self.gost_certificate_expiry_date = parse(bs.find(string='Сертификат ГОСТ').findNext('div').contents[0].split(' по ')[1])
                #self.rsa_certificate_expiry_date = soup.find_all("div", string="Сертификат RSA")
                self.up = True
                return True
            else:
                self.up = False
                return False
        except:
            self.up = False
            return False


if __name__ == '__main__':
    api = API('10.108.1.100', '8080')
    api.update()
    print(api.rsa_certificate_expiry_date)
    print(api.gost_certificate_expiry_date)