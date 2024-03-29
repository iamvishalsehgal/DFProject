from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.project import get_project_settings
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.utils.response import response_status_message
import random

class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent_list):
        self.user_agent_list = user_agent_list

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.user_agent_list))

class CustomRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if response.status == 403:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response
    

class AVCrawler(CrawlSpider):
    name = "AVCrawler"
    allowed_domains = ["etsy.com"]
    start_urls = ["https://www.etsy.com/"]

    rules = (
        Rule(LinkExtractor(allow="/listing")),
    )

    def __init__(self, *args, **kwargs):
        super(AVCrawler, self).__init__(*args, **kwargs)
        settings = get_project_settings()
        settings.set('ROBOTSTXT_OBEY', False)
        settings.set('DOWNLOAD_DELAY', 1)
        settings.set('AUTOTHROTTLE_ENABLED', True)

        # User-Agent Rotation
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0"
]

settings = get_project_settings()
settings.set('ROBOTSTXT_OBEY', False)
settings.set('DOWNLOAD_DELAY', 1)
settings.set('AUTOTHROTTLE_ENABLED', True)
settings.set('DOWNLOADER_MIDDLEWARES', {
    '__main__.RandomUserAgentMiddleware': 400,
    '__main__.CustomRetryMiddleware': 550,
})


    #rules = (
        # Extracting and follow all the links in /all path 
        #Rule(LinkExtractor(allow=""),follow = True),
        # Extract all the links other than /all and we define all the rules in parse_item functionn
        #Rule(LinkExtractor(allow="", deny="all"), callback="parse_item"),
        
    #)
# We are doing web scrapping here ,  Have to put correct css command to make it work so spend more time learning this

#    def parse_item(self, response):
        # Loop through each row in the table
#        for row in response.css('table#listtable tbody tr'):
#            yield (
#                'title': row.css('td.sorting_1 a::text').get().strip(),
            
            #"Search other databases":response.css(".editor-content a::text").getall(),
            #"title":response.css("td.sorting_1 a::text").get(),
#            )
        
#        next_page = response.css("li.next a::attr(href)").get()

#        if next_page is not None:
#            yield response.follow(next_page, callback= self.parse_item)
    
#To only scrape starting url
#    def parse_start_url(self, response):
#        return self.parse_item(response)
    
#    def parse_item(self, response):
#        pass
#        title = response.css('title::text').extract()
#        yield {'titletext': title}
        
#    def parse(self,response): #div_quote here is div tag and class name is quote so we named it like this.
#        all_div_quotes = response.css("div.quote")[0] #[0] is to extract 1st element instead of every, if we want to extract every then we can remove it.
#        title = all_div_quotes.css("span.text::text").extract()
#        author = all_div_quotes.css(".author::text").extract()
#        tag = all_div_quotes.css(".tag::text").extract()
#        yield {
#                "title":title,
#                "author":author,
#                "tag":tag
#        }