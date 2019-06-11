from .CrawlerBase import CrawlerBase


class CrawlerThreatfeedsIo(CrawlerBase):
    name = "Crawler for threatfeeds.io"

    def start(self):
        print("crawler started for threatfeeds.io")
        print("done crawling")
