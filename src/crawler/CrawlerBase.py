from abc import ABCMeta, abstractmethod

class CrawlerBase(metaclass=ABCMeta):
    @property
    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def get_IP_Records(self):
        pass

    @abstractmethod
    def get_IP_List_Records(self):
        pass
