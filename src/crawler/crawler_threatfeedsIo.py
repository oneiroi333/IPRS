import re
import json
from urllib import request, error

from bs4 import BeautifulSoup

from .crawler_base import CrawlerBase
from .crawler_result import CrawlerResult
from ..data_model import IP_List_Record, IP_Record
from ..utils import TIME_FRMT_LOG, print_log, extract_ip_addr_all


class CrawlerThreatfeedsIo(CrawlerBase):

    def __init__(self, verbose=False):
        self.verbose = verbose
        self._url = 'https://threatfeeds.io/'
        self._process_list_name = [ # Processing of these lists is implemented
            'Alienvault IP Reputation',
            'Bad IPs',
            'BBcan177 Malicious IPs',
            'Blocklist.de Blocklist',
            'Botvrij.eu - ips',
            'C&C IPs',
            'CI Bad Guys',
            'Compromised IPs',
            # TODO 'Darklist',
            'Dictionary SSH Attacks',
            'GreenSnow Blacklist',
            'Hancitor IPs',
            'High Confidence IPv4 Drop List',
            'IPSpamList',
            'Ransomware IPs',
            'SSL BL',
            'Talos IP Blacklist',
            'Tor IPs', # allows download every 30min
            'Zeus Bad IPs'
        ]
        self._ip_records = {} # { IP_Record.ip_address : IP_Record }
        self._iplist_records = {} # { IP_List_Record.name : IP_List_Record }
        self._ip_to_iplist_map = {} # { ip_address: [name1, name2] }

    def start(self):
        html = request.urlopen(self._url).read()
        soup = BeautifulSoup(html, 'html.parser')
        script_raw = str(soup.find(id='content').find('script')) \
                        .replace('\n', '') \
                        .replace('\t', '')
        try:
            # Grep the feeds from script
            feeds_raw = re.search(r'(?<=var feeds = )[^;]+', script_raw).group()
            # Remove escape chars
            feeds_raw = re.sub(r'\\(.)', r'\1', feeds_raw)
        except:
            # Unable to get the feeds
            return
        feeds_dict = json.loads(feeds_raw)
        # Filter for free accessible lists
        feeds_list = list(filter(lambda e: e['pricing'] == 'free', feeds_dict))

        for feed in feeds_list:
            if feed.get('name') and feed.get('name') in self._process_list_name:
                if self.verbose:
                    print_log(TIME_FRMT_LOG, '[{}] Processing feed: \'{}\''.format(self.__class__.__name__, feed.get('name')))

                name = feed.get('name')
                managed_by_name = feed.get('author')
                managed_by_url = feed.get('website')
                fetch_url = feed.get('url')
                if not fetch_url:
                    if self.verbose:
                        print_log(TIME_FRMT_LOG, '[{}] [ERROR] Processing feed: \'{}\': {}'.format(self.__class__.__name__, feed.get('name'), 'no url to fetch from'))
                    continue
                try:
                    # Some urls require a user-agent to get the data, so lets set a simple one
                    req = request.Request(
                        fetch_url,
                        headers = {'User-Agent': 'Mozilla/5.0'}
                    )
                    data = request.urlopen(req).read()
                except error.URLError as err:
                    # Unable to get the data
                    if self.verbose:
                        print_log(TIME_FRMT_LOG, '[{}] [ERROR] Processing feed: \'{}\': {}'.format(self.__class__.__name__, feed.get('name'), err))
                    continue

                iplist_rec = IP_List_Record(
                    name = name,
                    src_url = self._url,
                    fetch_url = fetch_url,
                    managed_by = {
                        'name': managed_by_name,
                        'url': managed_by_url
                    }
                )
                self._iplist_records.update({name: iplist_rec})

                self._process_list(name, data)
                
    def get_result(self):
        return CrawlerResult(self._ip_records, self._iplist_records, self._ip_to_iplist_map)

    def _process_list(self, name, data):
        ip_addr_all = {
            'ipv4': set(),
            'ipv6': set()
        }

        # Handle the different lists
        if name in [
                'Bad IPs', 'Blocklist.de Blocklist', 'Botvrij.eu - ips', 'CI Bad Guys',
                'Compromised IPs', 'GreenSnow Blacklist', 'Ransomware IPs', 'Talos IP Blacklist',
                'Tor IPs', 'Zeus Bad IPs'
            ]:
            ip_addr_all = extract_ip_addr_all(data)
        elif name in [
                'Alienvault IP Reputation', 'BBcan177 Malicious IPs', 'Brute Force Blocker',
                'Hancitor IPs'
            ]:
            try:
                data = '\n'.join([line.split('#')[0] for line in data.decode().splitlines()])
            except:
                return
            ip_addr_all = extract_ip_addr_all(data)
        elif name in ['C&C IPs']:
            try:
                data = '\n'.join([line.split(',')[0] for line in data.decode().splitlines()])
            except:
                return
            ip_addr_all = extract_ip_addr_all(data)
        elif name in ['Darklist']:
            # TODO process cidr ips
            pass
        elif name in ['Dictionary SSH Attacks']:
            try:
                data = '\n'.join([line.split(':')[1] for line in data.decode().splitlines()])
            except:
                return
            ip_addr_all = extract_ip_addr_all(data)
        elif name in ['High Confidence IPv4 Drop List']:
            try:
                data = '\n'.join([line.split('-')[0] for line in data.decode().splitlines()])
            except:
                return
            ip_addr_all = extract_ip_addr_all(data)
        elif name in ['IPSpamList']:
            try:
                data = '\n'.join([line.split(',')[2] for line in data.decode().splitlines()])
            except:
                return
            ip_addr_all = extract_ip_addr_all(data)
        elif name in ['SSL BL']:
            try:
                data = '\n'.join([line.split(',')[1] for line in data.decode().splitlines()])
            except:
                return
            ip_addr_all = extract_ip_addr_all(data)

        for ip_version in ip_addr_all:
            for ip_addr in ip_addr_all[ip_version]:
                # Add ip if it doesnt exist already
                if not self._ip_records.get(ip_addr):
                    ip_rec = IP_Record()
                    ip_rec.ip_address = ip_addr
                    ip_rec.ip_version = 4 if ip_version == 'ipv4' else 6
                    if name in ['C&C IPs']:
                        ip_rec.tags['cc'] = True
                    elif name in ['Tor IPs']:
                        ip_rec.tags['tor_node'] = True

                    self._ip_records.update({ip_addr: ip_rec})
                # Map the ip to the list
                lists = self._ip_to_iplist_map.get(ip_addr)
                if lists:
                    lists.append(name)
                else:
                    lists = [name]
                self._ip_to_iplist_map.update({ip_addr: lists})

