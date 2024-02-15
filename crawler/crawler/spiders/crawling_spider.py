from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "Crawler"
    allowed_domains = ["uvt.nl"] # domain link
    start_urls = ["https://libsearch.uvt.nl/"] # website link 

    rules = (
        # all here is the https://libsearch.uvt.nl/all/ loction where books are kinda
        Rule(LinkExtractor(allow=("all")), callback='parse_item', follow=True),
)
