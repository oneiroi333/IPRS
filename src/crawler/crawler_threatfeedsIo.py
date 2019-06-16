import re
import requests
from selenium import webdriver

from .crawler_base import CrawlerBase
from .crawler_result import CrawlerResult
from ..data_model import IP_List_Record, IP_Record


class CrawlerThreatfeedsIo(CrawlerBase):

    '''
    Requires the binaries:
        chrome
        chromedriver
    '''

    def __init__(self):
        self._url = 'https://threatfeeds.io/'
        self._webdriver_conf = {
            'chrome_path': None,
            'chromedriver_path': None
        }
        self._process_list_name = [ # Processing of these lists is implemented
            'Botvrij.eu - ips',
            'Zeus Bad IPs'
        ]
        self._ip_records = {} # { IP_Record.ip_address : IP_Record }
        self._iplist_records = {} # { IP_List_Record.name : IP_List_Record }
        self._ip_to_iplist_map = {} # { ip_address: [name1, name2] }

    def start(self):
        chrome_options = webdriver.chrome.options.Options() 
        chrome_options.add_argument('--headless') # without UI
        if self._webdriver_conf['chrome_path']:
            chrome_options.binary_location = self._webdriver_conf['chrome_path']
        if self._webdriver_conf['chromedriver_path']:
            driver = webdriver.Chrome(
                executable_path = self._webdriver_conf['chromedriver_path'],
                chrome_options = chrome_options
            )
        else:
            driver = webdriver.Chrome(options=chrome_options)
        driver.get(self._url)

        # Get the list metadata
        results = driver.find_element_by_id('results')
        items = results.find_elements_by_css_selector('div.item')
        for item in items:
            # get rid of sponsored lists cause we cant access them for free(?)
            if 'sponsored' in item.get_attribute('class'):
                continue

            try:
                name = item.find_element_by_css_selector('div.name').text
            except:
                # The list name is the only information we have to know if we can process the list or not
                continue
            # Check if we implemented the processing of this list
            if name not in self._process_list_name:
                continue
            try:
                infoblock = item.find_element_by_css_selector('div.infoblock')
                managed_by_name = infoblock.find_element_by_css_selector('div.author').text
            except:
                managed_by_name = None
            try:
                managed_by_url = infoblock.find_element_by_tag_name('a').get_attribute('href')
            except:
                managed_by_url = None

            # Get the actual list data
            try:
                data_url = item.find_element_by_css_selector('div.stats').find_element_by_css_selector('a.button').get_attribute('href')
            except:
                continue

            # FUTURE IMPROVEMENT
            # Should only fetch the data if the list got modified since the last fetch (date_last_fetch)
            # This date information has to come from the database and somehow passed to the crawler (true for every crawler)

            resp = requests.get(data_url)
            if resp.status_code != requests.codes.ok:
                continue
            data = resp.text

            iplist_rec = IP_List_Record(
                name = name,
                src_url = self._url,
                fetch_url = data_url,
                managed_by = {
                    'name': managed_by_name,
                    'url': managed_by_url
                }
            )
            self._iplist_records.update({name: iplist_rec})

            # Process the data depending on the list
            self._process_list(name, data)

        driver.quit()

    def get_result(self):
        return CrawlerResult(self._ip_records, self._iplist_records, self._ip_to_iplist_map)

    def _process_list(self, name, data):
        ip_addr_list = None
        if 'Botvrij.eu - ips' in name:
            ip_addr_list = data.splitlines()
        elif 'Zeus Bad IPs' in name:
            ip_addr_list = re.findall(r'[0-9]+(?:\.[0-9]+){3}', data)

        if ip_addr_list:
            for ip_addr in ip_addr_list:
                ip_addr = ip_addr.strip()

                if not self._ip_records.get(ip_addr):
                    ip_rec = IP_Record()
                    ip_rec.ip_address = ip_addr
                    self._ip_records.update({ip_addr: ip_rec})

                lists = self._ip_to_iplist_map.get(ip_addr)
                if lists:
                    lists.append(name)
                else:
                    lists = [name]
                self._ip_to_iplist_map.update({ip_addr: lists})

