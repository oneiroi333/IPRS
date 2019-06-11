import requests
from bs4 import BeautifulSoup

from .CrawlerBase import CrawlerBase
from ...data_model.IP_Record import IP_Record
from ...data_model.IP_List_Record import IP_List_Record

class CrawlerThreatfeedsIo(CrawlerBase):
    def __init__(self):
        self.url = 'https://threatfeeds.io/'
        self.ip_records = []
        self.ip_list_records = []

    def start(self):
        resp = requests.get(self.url)
        if not resp.statusCode == 200:
            return

        soup = BeautifulSoup(resp.content, 'html.parser')
        # Find all blacklists
        lists = soup.find(class_='item')

    def get_IP_Records(self):
        return self.ip_records

    def get_IP_List_Records(self):
        return self.ip_list_records

