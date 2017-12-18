import requests, math, time, scrapy, logging, json, pandas as pd
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.selector import HtmlXPathSelector

final = []

dfjson = pd.read_json('assets/data/urls_to_scrape.json')
for i in range(len(dfjson['link'])):
    for j in dfjson['link'][i]:
        final.append(j)
df_final = pd.DataFrame(final).drop_duplicates()

final_url = df_final[0].tolist()

# Use Scrapy to start scraping for the urls
class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('assets/data/data.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class ExtractSpider(scrapy.Spider):
    name = "Extract"
    start_urls = final_url

    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1}, # Used for pipeline 1
        'FEED_FORMAT':'json',                                 # Used for pipeline 2
        'FEED_URI': 'assets/data/data.json'                        # Used for pipeline 2
    }

    def parse(self, response):
        # for user in response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tbody'):
        #     yield {
        #         # https://stackoverflow.com/questions/20081024/scrapy-get-request-url-in-parse
        #         'Property_ID': user.xpath('tr[1]/td').extract()
        #     }
        yield {
            'link': response.url,
            'scraping date': time.strftime("%m/%d/%Y"),
            'Property_ID': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[1]/td/text()').extract(),
            'Status': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[2]/td/text()').extract(),
            'Price': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[3]/td/div[1]/text()').extract(),
            'Price per feet(built-up)': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[4]/td/div/text()').extract(),
            'Price per feet(salesable area)': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[5]/td/div/text()').extract(),
            'Gross area(sq feet)': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[6]/td/text()').extract(),
            'Net floor area(sq feet)': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[7]/td/text()').extract(),
            'Property age(year)': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[8]/td/text()').extract(),
            'Address': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[9]/td/div/div[1]/text()').extract(),
            'Address link': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[9]/td/div/div[2]/a/@href').extract(),
            'Views': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[10]/td/text()').extract(),
            'Bookmarked': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[11]/td/text()').extract(),
            'Ads or renew date': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[12]/td/text()').extract(),
            'Modified date': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[13]/td/text()').extract(),
            'User last login': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[14]/td/text()').extract(),
            'Expire date': response.xpath('//*[@id="bA"]/div[2]/div[2]/ul/li[1]/div/div[1]/table/tr[15]/td/text()').extract(),
        }

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'
})

process.crawl(ExtractSpider)
process.start()
