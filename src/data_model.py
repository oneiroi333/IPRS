from datetime import datetime


class IP_List_Record:

    def __init__(self,
            name = None,
            date_created = datetime.now(),
            date_last_fetch = datetime.now(),
            src_url = None,
            fetch_url = None,
            managed_by = {
                'name': None,
                'url': None
            }
            ):
        self.name = name
        self.date_created = date_created
        self.date_last_fetch = date_last_fetch
        self.src_url= src_url
        self.fetch_url= fetch_url
        self.managed_by = managed_by


class IP_Record:

    def __init__(self,
            ip_address = None,
            ip_version = 4,
            date_created = datetime.now(),
            date_last_seen = datetime.now(),
            tags = {
                'proxy': False,
                'tor_node': False,
                'malware': False,
                'cc': False,
                'spam': False,
                'compromised': False,
                'attacker': False
            },
            whois = None,
            iplist_refs = []
            ):
        self.ip_address = ip_address
        self.ip_version = ip_version
        self.date_created = date_created
        self.date_last_seen = date_last_seen
        self.tags = tags
        self.whois = whois
        self.iplist_refs = iplist_refs
