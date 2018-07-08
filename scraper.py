import scrapy, time, logging, json, pandas as pd
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.selector import HtmlXPathSelector


### TODO
# sync google cloud/aws/zaure free

# Default url
main_urls = ['https://www.28hse.com/en/buy/place-1/house-type-g1','https://www.28hse.com/en/buy/place-2/house-type-g1','https://www.28hse.com/en/buy/place-3/house-type-g1']


def scrapers(urls = main_urls, file_format = '.csv', next_page_dummy = True, file_path = 'assets/data/urls_to_scrape_'+ time.strftime("%m-%d-%Y") ):

    # Use Scrapy to start scraping for the urls
    class JsonWriterPipeline(object):

        def open_spider(self, spider):
            self.file = open('assets/data/urls_to_scrape_'+ time.strftime("%m-%d-%Y")+'.jl', 'w')

        def close_spider(self, spider):
            self.file.close()

        def process_item(self, item, spider):
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
            return item

    class ExtractSpider(scrapy.Spider):
        name = "Extract"
        start_urls = main_urls

        custom_settings = {
            'LOG_LEVEL': logging.WARNING,
            # 'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1}, # Used for pipeline 1
            'FEED_FORMAT': file_format,                                 # Used for pipeline 2
            'FEED_URI': 'assets/data/urls_to_scrape_'+ time.strftime("%m-%d-%Y")+ file_format         # Used for pipeline 2
        }

        def parse(self, response):
            links = response.xpath('//*[@id="search_main_div"]/div/ul/li[1]/div[2]/p[1]/a/@href').extract()
            for listing in links:
                yield scrapy.Request(listing, callback=self.parse_detail_page)



                # To scrape from listing page - only summary
                # {
                #     # https://stackoverflow.com/questions/20081024/scrapy-get-request-url-in-parse
                #     'Link'          : listing.xpath('div/ul/li[1]/div[2]/p[1]/a/@href').extract(),
                #     'District'      : listing.xpath('div/ul/li[1]/div[2]/div[1]/a[1]/text()').extract(),
                #     'District Link' : listing.xpath('div/ul/li[1]/div[2]/div[1]/a[1]/@href').extract(),
                #     'Estate'        : listing.xpath('div/ul/li[1]/div[2]/div[1]/a[2]/text()').extract(),
                #     'Estate Link'   : listing.xpath('div/ul/li[1]/div[2]/div[1]/a[2]/@href').extract(),
                #     'Price'         : listing.xpath('div/ul/li[2]/div/text()').extract(),
                #     'GFA'           : listing.xpath('div/ul/li[1]/div[2]/p[2]/text()').extract(),
                #     'SA'            : listing.xpath('div/ul/li[1]/div[2]/p[3]/text()').extract(),
                # }

            if next_page_dummy is True:
                # finds the next page and click the next page to reprocess everything    
                next_page = response.xpath('//a[contains(text(), "next")]/@href').extract()
                # print(next_page) 
                if next_page:
                    yield scrapy.Request(
                        response.urljoin(next_page[0]),
                        callback=self.parse
                    )

        def parse_detail_page(self, response):
            
            # have to set it to be a scrapy field to be returned above? https://github.com/kadnan/OlxScraper/blob/master/olx/spiders/electronics.py
            houses = scrapy.Field()

            # https://stackoverflow.com/questions/34002785/scrapy-script-how-to-find-specific-keyword-and-return-or-print-url
            houses['Region']                         = response.xpath('//*[@class="clearfix header_linkage_28hse"]/div[1]/a[5]/text()').extract()
            houses['Region Link']                    = response.xpath('//*[@class="clearfix header_linkage_28hse"]/div[1]/a[5]/@href').extract()
            houses['Estate']                         = response.xpath('//*[@class="clearfix header_linkage_28hse"]/div[1]/a[6]/text()').extract()
            houses['Estate Link']                    = response.xpath('//*[@class="clearfix header_linkage_28hse"]/div[1]/a[6]/@href').extract()
            houses['ID']                             = response.xpath('//*[@class="table_info"]/div[1]/table/tr[1]/td/text()').extract()
            houses['Status']                         = response.xpath('//*[@class="table_info"]/div[1]/table/tr[2]/td/text()').extract()
            houses['Price']                          = response.xpath('//*[@class="table_info"]/div[1]/table/tr[3]/td/div[1]/text()').extract()
            houses['Price per feet(built-up)']       = response.xpath('//th[contains(text(), "Price per feet(built-up)")]/following::div[1]/text()').extract()
            houses['Price per feet(salesable area)'] = response.xpath('//th[contains(text(), "Price per feet(salesable area)")]/following::div[1]/text()').extract()
            houses['Block and unit number']          = response.xpath('//th[contains(text(), "Block and unit number")]/following::td[1]/text()').extract()
            houses['Floor']                          = response.xpath('//th[contains(text(), "Floor")]/following::td[1]/text()').extract()
            houses['Room']                           = response.xpath('//th[contains(text(), "Room")]/following::td[1]/text()').extract()
            houses['Gross area(sq feet)']            = response.xpath('//th[contains(text(), "Gross area(sq feet)")]/following::td[1]/text()').extract()
            houses['Net floor area(sq feet)']        = response.xpath('//th[contains(text(), "Net floor area(sq feet)")]/following::td[1]/text()').extract()
            houses['Management Fee']                 = response.xpath('//th[contains(text(), "Management Fee")]/following::td[1]/text()').extract()
            houses['Property age(year)']             = response.xpath('//th[contains(text(), "Property age(year)")]/following::td[1]/text()').extract()
            houses['Address']                        = response.xpath('//th[contains(text(), "Address")]/following::td[1]/text()').extract()
            houses['Views #']                        = response.xpath('//th[contains(text(), "Views #")]/following::td[1]/text()').extract()
            houses['Bookmarked #']                   = response.xpath('//th[contains(text(), "Bookmarked #")]/following::td[1]/text()').extract()
            houses['Ads or renew date']              = response.xpath('//th[contains(text(), "Ads or renew date")]/following::td[1]/text()').extract()
            houses['Modified date']                  = response.xpath('//th[contains(text(), "Modified date")]/following::td[1]/text()').extract()
            houses['User last login']                = response.xpath('//th[contains(text(), "User last login")]/following::td[1]/text()').extract()
            houses['Expire date']                    = response.xpath('//th[contains(text(), "Expire date")]/following::td[1]/text()').extract()
            houses['Scrape Date']                    = time.strftime("%m-%d-%Y")
            yield houses


    process = CrawlerProcess({ 'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' })

    process.crawl(ExtractSpider)
    process.start()


# https://www.digitalocean.com/community/tutorials/how-to-crawl-a-web-page-with-scrapy-and-python-3


### Old way ####
# # use Request & BeautifulSoup
# r = requests.get(main_urls[0],headers=headers)
# soup = BeautifulSoup(r.text,"lxml")

# # Get the number of results
# result = soup.find('div', class_='search_total_result')
# num_result = float(result.find('em').string)
# # Number of pages
# pages = math.ceil(num_result/15)

# print('There are {} pages'.format(pages))
