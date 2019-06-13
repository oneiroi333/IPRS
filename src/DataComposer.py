from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from .crawler.CrawlerManager import CrawlerManager


class DataComposer():

    def __init__(self, verbose=False, host='localhost', port=27017, user=None, pw=None):
        self.verbose = verbose
        self.mongodb = {
            'host': host,
            'port': port,
            'user': user,
            'pw': pw
        }
        self._crawler_manager = CrawlerManager(
            verbose = self.verbose,
            crawler_result_callback = self._process_crawler_result
        )

    def start(self):
        """
        client = MongoClient()
        # Check connection to the mongo db
        try:
            client.admin.command('ismaster')
        except ConnectionFailure:
            print('Connection to MongoDB failed')
            return
        """
        self._crawler_manager.start()

    def _process_crawler_result(self, crawler_result):
        print("Lists fetched:")
        for iplist_rec in crawler_result.iplist_records:
            print(crawler_result.iplist_records[iplist_rec].name)
