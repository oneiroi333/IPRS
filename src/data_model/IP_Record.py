from datetime import datetime

class IP_Record:
    def __init__(self,
            ip_address,
            ip_version = 4,
            date_created = datetime.now(),
            date_first_seen = datetime.now(),
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
            ip_list_ids = []
        ):
        self.ip_address = ipAaddress
        self.ip_version = ip_version
        self.date_created = date_created
        self.date_first_seen = date_first_seen
        self.date_last_seen = date_last_seen
        self.tags = tags
        self.whois = whois
        self.ip_list_ids = ip_list_ids
