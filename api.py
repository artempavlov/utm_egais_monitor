from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse


def get_status(ip, port):
    status = {
        'is_up': None,
        'status_code': None,
        'rsa_certificate_expiry_date': None,
        'gost_certificate_expiry_date': None,
    }
    try:
        r = requests.get('http://'+ip+':'+port)
        status['status_code'] = r.status_code
        if r.status_code == 200:
            bs = BeautifulSoup(r.text, features="lxml")
            status['rsa_certificate_expiry_date'] = \
                parse(bs.find(string='Сертификат RSA').findNext('div').contents[0].split(' по ')[1])
            status['gost_certificate_expiry_date'] = \
                parse(bs.find(string='Сертификат ГОСТ').findNext('div').contents[0].split(' по ')[1])
            status['is_up'] = True
            return status
        else:
            status['is_up'] = False
            return status
    except requests.exceptions.RequestException:
        status['is_up'] = False
        return status
