from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AVCrawler(CrawlSpider):
    name = "AVCrawler"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

#Rules also include extracting all urls
#    rules = (
#        Rule(LinkExtractor(allow=()), callback='parse_item'),
#    )

#To only scrape starting url
    def parse_start_url(self, response):
        return self.parse_item(response)
    
    def parse_item(self, response):
#        title = response.css('title::text').extract()
#        yield {'titletext': title}