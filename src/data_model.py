from datetime import datetime


class IP_List_Record:

    def __init__(self,
            name,
            date_created = datetime.now(),
            date_last_fetch = datetime.now(),
            src_url = None,
            fetch_url = None,
            managed_by_name = None,
            managed_by_url = None
        ):
        self.name = name
        self.date_created = date_created
        self.date_last_fetch = date_last_fetch
        self.src_url= src_url
        self.fetch_url= fetch_url
        self.managed_by = {
            'name': managed_by_name,
            'url': managed_by_url
        }


class IP_Record:

    def __init__(self,
            ip_address,
            ip_version = 4,
            date_created = datetime.now(),
            date_last_seen = datetime.now(),
            whois = None
        ):
        self.ip_address = ip_address
        self.ip_version = ip_version
        self.date_created = date_created
        self.date_last_seen = date_last_seen
        self.tags = {
            'proxy': False,
            'tor_node': False,
            'malware': False,
            'cc': False,
            'spam': False,
            'compromised': False,
            'attacker': False
        }
        self.whois = whois
        self.iplist_refs = []
