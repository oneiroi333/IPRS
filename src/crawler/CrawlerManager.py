from datetime import datetime
from .CrawlerBase import CrawlerBase


class CrawlerManager:
    """
    Manages the starting of multiple crawler

    TODO start thread/process for every crawler?
    """
    def __init__(self):
        self.registeredCrawler = []

    def registerCrawler(self, crawler):
        """
        Register a crawler for execution
        """
        if (not isinstance(crawler, CrawlerBase)):
                raise TypeError('Invalid crawler: crawler must be of instance CrawlerBase')
        self.registeredCrawler.append(crawler)

    def start(self):
        """
        Start executing all registered crawler
        """
        timefrmt = '%H:%M:%S' 

        for crawler in self.registeredCrawler:
            starttime = datetime.now().strftime(timefrmt)
            print('[{}] Starting Crawler: {}'.format(starttime, crawler.name))
            crawler.start()
            endtime = datetime.now().strftime(timefrmt)
            print('[{}] Finished'.format(endtime))
