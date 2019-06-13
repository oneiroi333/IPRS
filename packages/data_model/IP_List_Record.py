from datetime import datetime

class IP_List_Record:

    def __init__(self,
            name = None,
            date_created = datetime.now(),
            date_last_fetch = datetime.now(),
            src_url = None,
            managed_by = {
                'name': None,
                'url': None
            }
            ):
        self.name = name
        self.date_created = date_created
        self.date_last_fetch = date_last_fetch
        self.src_url= src_url
        self.managed_by = managed_by
