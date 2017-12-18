import requests, math, scrapy, logging, json, pandas as pd
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.selector import HtmlXPathSelector

urls = ['https://www.28hse.com/en/buy/house-type-g1']

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

r = requests.get('https://www.28hse.com/en/buy/house-type-g1',headers=headers)

soup = BeautifulSoup(r.text,"lxml")

# Get the number of results
result = soup.find('div', class_='search_total_result')

num_result = float(result.find('em').string)

# Number of pages
pages = math.ceil(num_result/15)
print('There are {} pages'.format(pages))

# from page 2 to pages
base_url = 'https://www.28hse.com/en/buy/house-type-g1/list-'

i = 2
while i < pages + 1:
	url = base_url + str(i)
	urls.append(url)
	i += 1

# Use Scrapy to start scraping for the urls
class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('assets/data/urls_to_scrape.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class ExtractSpider(scrapy.Spider):
    name = "Extract"
    start_urls = urls

    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1}, # Used for pipeline 1
        'FEED_FORMAT':'json',                                 # Used for pipeline 2
        'FEED_URI': 'assets/data/urls_to_scrape.json'                        # Used for pipeline 2
    }

    def parse(self, response):
        for user in response.xpath('//*[@id="search_main_div"]'):
            yield {
                # https://stackoverflow.com/questions/20081024/scrapy-get-request-url-in-parse
                'link': user.xpath('div/ul/li[1]/div[2]/p[1]/a/@href').extract()

            }

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'
})

process.crawl(ExtractSpider)
process.start()
