import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging
import os

class WalletSpider(CrawlSpider):
    name = 'wallet_spider'
    allowed_domains = ['playerup.com']
    start_urls = ['https://www.playerup.com/middleman/?page_id=5&form=pay_way']

    rules = (
        Rule(LinkExtractor(allow=r'/middleman/payment/[\w-]+\.php$'), callback='parse_wallet', follow=True),
    )



    def parse_wallet(self, response):
        wallet_addresses = {}

        payment_options = response.css('p.style6').extract()
        for option in payment_options:
            option_text = scrapy.Selector(text=option).css('span.style1::text').getall()
            option_text = ' '.join(option_text).strip()
            
            if 'Address:' in option_text:
                parts = option_text.split('Address:')
                for i in range(1, len(parts)):
                    type_part = parts[i-1].strip().split()[-1].strip()
                    address_part = parts[i].strip().split()[0].strip()
                    wallet_addresses[type_part] = address_part

        if wallet_addresses:
            yield {
                'url': response.url,
                'wallet_addresses': wallet_addresses
            }
        else:
            logging.warning(f"No wallet addresses found on page: {response.url}")
