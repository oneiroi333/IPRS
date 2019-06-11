from abc import ABCMeta, abstractmethod


class CrawlerBase(metaclass=ABCMeta):
    """
    Crawler base class. Crawler must inherit from this class
    """
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def start(self):
        pass
