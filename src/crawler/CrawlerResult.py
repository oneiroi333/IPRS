class CrawlerResult():

    def __init__(self, ip_records, iplist_records, ip_to_iplist_map):
        # Dict: { IP_Record.ip_address : IP_Record }
        self.ip_records = ip_records
        # Dict { IP_List_Record.name : IP_List_Record }
        self.iplist_records = iplist_records
        # Dict { IP_Record.ip_address : [ IP_List_Record.name1, IP_List_Record.name2 ] }
        self.ip_to_iplist_map = ip_to_iplist_map
