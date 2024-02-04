from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "Crawler"
    allowed_domains = ["uvt.nl"]
    start_urls = ["http://libsearch.uvt.nl"]

    rules = (
        # all here is the https://libsearch.uvt.nl/all/ loction where books are kinda
        Rule(LinkExtractor(allow="all"),),
    )
