from abc import ABC, abstractmethod


class CrawlerBase(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def get_result(self):
        '''
        Return a CrawlerResult object
        '''
        pass
