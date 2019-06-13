from abc import ABC, abstractmethod


class CrawlerBase(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def get_results(self):
        '''
        Return a tuple containing:
        1) Dict: { IP_Record.ip_address : IP_Record }
        2) Dict: { IP_List_Record.name : IP_List_Record }
        3) Dict: { IP_Record.ip_address : [ IP_List_Record.name1, IP_List_Record.name2 ] }
        '''
        pass
