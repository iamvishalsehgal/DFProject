from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

proxies = { 
     'http': 'localhost:8118',
     'https': 'localhost:8118'
}

class CrawlingSpider(CrawlSpider):
    name = "AVCrawler"
    allowed_domains = ["muwgjdckwwmhyi7lj73dspumrxmzuzjvujmtmyrhhbjrgswcakobtfad.onion"] # domain link
    start_urls = ["https://muwgjdckwwmhyi7lj73dspumrxmzuzjvujmtmyrhhbjrgswcakobtfad.onion/"] # website link 

    rules = (
        # all here is the https://libsearch.uvt.nl/all/ loction where books are kinda
        Rule(LinkExtractor(allow=("all")), callback='parse_item', follow=True),
)
