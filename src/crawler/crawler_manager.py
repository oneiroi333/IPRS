from .crawler_threatfeedsIo import CrawlerThreatfeedsIo
from ..utils import print_log, TIME_FRMT_LOG


class CrawlerManager:

    def __init__(self, verbose=False, crawler_result_callback=None):
        self.verbose = verbose
        self.crawler_result_callback = crawler_result_callback
        self._crawler = [
            CrawlerThreatfeedsIo(verbose),
        ]
        self._time_frmt_log = TIME_FRMT_LOG

    def start(self):
        if self.verbose:
            print_log(self._time_frmt_log, '[{}] Start'.format(self.__class__.__name__))
        for crawler in list(self._crawler):
            crawler_name = type(crawler).__name__

            if self.verbose:
                print_log(self._time_frmt_log, '[{}] Start crawler: {}'.format(self.__class__.__name__, crawler_name))
            crawler.start()
            if self.verbose:
                print_log(self._time_frmt_log, '[{}] Crawler finished: {}'.format(self.__class__.__name__, crawler_name))

            if self.verbose:
                print_log(self._time_frmt_log, '[{}] Start processing results: {}'.format(self.__class__.__name__, crawler_name))
            self.crawler_result_callback(crawler.get_result())
            if self.verbose:
                print_log(self._time_frmt_log, '[{}] Finished processing results: {}'.format(self.__class__.__name__, crawler_name))
            # Remove the crawler from the list to delete the instances and their memory usage
            self._crawler.remove(crawler)
        if self.verbose:
            print_log(self._time_frmt_log, '[{}] Finish'.format(self.__class__.__name__))

