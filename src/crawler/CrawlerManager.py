from datetime import datetime

from .CrawlerThreatfeedsIo import CrawlerThreatfeedsIo


class CrawlerManager:

    def __init__(self, verbose=False, crawler_result_callback=None):
        self.verbose = verbose
        self.crawler_result_callback = crawler_result_callback
        self._crawler = [
            CrawlerThreatfeedsIo(),
        ]
        self._timefrmt_log = '%H:%M:%S'

    def start(self):
        self._print_log('Start: {}'.format(type(self).__name__))

        # TODO: multiprocessing/-threading of crawlers
        for crawler in self._crawler:
            crawler_name = type(crawler).__name__

            self._print_log('Start crawling: {}'.format(crawler_name))
            crawler.start()
            self._print_log('Finished crawling: {}'.format(crawler_name))

            self._print_log('Start processing results: {}'.format(crawler_name))
            self.crawler_result_callback(crawler.get_result())
            self._print_log('Finished processing results: {}'.format(crawler_name))

    def _print_log(self, msg):
        if self.verbose:
            print('[{}] {}'.format(datetime.now().strftime(self._timefrmt_log), msg))
