import requests
from bs4 import BeautifulSoup

from .CrawlerBase import CrawlerBase

# from data_model.IP_Record import IP_Record
# from data_model.IP_List_Record import IP_List_Record

class CrawlerThreatfeedsIo(CrawlerBase):
    def __init__(self):
        self.url = 'https://threatfeeds.io/'
        self.ip_records = {} # ip_address : IP_Record
        self.iplist_records = {} # name : IP_List_Record
        self.ip_to_iplist_map = {} # ip_address: [name1, name2]

    def start(self):
        resp = requests.get(self.url)
        resp.raise_for_status() # if resp.status != 200: raise http_error

        soup = BeautifulSoup(resp.text, 'html.parser')
        list_wrapper = soup.find(id='results')
        print(list_wrapper)
        print(list_wrapper.contents)
        print(list_wrapper.contents[0])
        lists = list_wrapper.find_all(class_='item')
        print(lists)
        for list_ in lists:
            list_name = list_.find(class_='name').string
            print(list_name)

    def get_ip_records(self):
        return self.ip_records

    def get_iplist_records(self):
        return self.iplist_records

    def get_ip_to_iplist_map(self):
        return self.ip_to_iplist_map
