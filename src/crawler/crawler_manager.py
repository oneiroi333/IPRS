from .crawler_threatfeedsIo import CrawlerThreatfeedsIo
from ..utils import print_log, TIME_FRMT_LOG


class CrawlerManager:

    def __init__(self, verbose=False, crawler_result_callback=None):
        self.verbose = verbose
        self.crawler_result_callback = crawler_result_callback
        self._crawler = [
            CrawlerThreatfeedsIo(),
        ]
        self._time_frmt_log = TIME_FRMT_LOG

    def start(self):
        if self.verbose:
            print_log(self._time_frmt_log, 'Start: {}'.format(type(self).__name__))

        for crawler in list(self._crawler):
            crawler_name = type(crawler).__name__

            if self.verbose:
                print_log(self._time_frmt_log, 'Start crawling: {}'.format(crawler_name))
            crawler.start()
            if self.verbose:
                print_log(self._time_frmt_log, 'Finished crawling: {}'.format(crawler_name))

            if self.verbose:
                print_log(self._time_frmt_log, 'Start processing results: {}'.format(crawler_name))
            self.crawler_result_callback(crawler.get_result())
            if self.verbose:
                print_log(self._time_frmt_log, 'Finished processing results: {}'.format(crawler_name))
            # Remove the crawler from the list to delete the instances and their memory usage
            self._crawler.remove(crawler)

