from datetime import datetime
from .CrawlerBase import CrawlerBase

class CrawlerManager:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self._crawler = []

    def register_crawler(self, crawler):
        if (not isinstance(crawler, CrawlerBase)):
                raise TypeError('Invalid crawler: crawler must inherit from abstract class CrawlerBase')
        self._crawler.append(crawler)

    def start(self):
        timefrmt = '%H:%M:%S' 

        for crawler in self._crawler:
            if self.verbose:
                starttime = datetime.now().strftime(timefrmt)
                print('[{}] Start crawling: {}'.format(starttime, crawler.url))

            crawler.start()

            if self.verbose:
                endtime = datetime.now().strftime(timefrmt)
                print('[{}] Finished crawling: {}'.format(starttime, crawler.url))
