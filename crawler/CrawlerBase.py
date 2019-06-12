from abc import ABCMeta, abstractmethod

class CrawlerBase(metaclass=ABCMeta):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def get_ip_records(self):
        pass

    @abstractmethod
    def get_iplist_records(self):
        pass

    @abstractmethod
    def get_ip_to_iplist_map(self):
        pass
