import requests, math, scrapy, logging, json, pandas as pd
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.selector import HtmlXPathSelector

dfjson = pd.read_json('urls_to_scrape.json')
print(dfjson.head())
