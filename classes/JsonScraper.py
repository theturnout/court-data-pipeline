from scrapy.crawler import CrawlerProcess
# from spiders.JsonSpider import JsonSpider
import regex as re
import json
import csv
import requests
import datetime
import scrapy


class JsonScraper(scrapy.Spider):

    name = "court_data_spider"

    def __init__(self, urls='', *args, **kwargs):
        super(JsonScraper, self).__init__(*args, **kwargs)
        self.urls = urls

    json_list = []

    def start_requests(self):

        print("Starting web scraper.")

        # GET request, pass response to parse()
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):

        print("starting parse()")
        try:
            # look for json data.
            linked_json = response.selector.xpath(
                '//link[@type="application/ld+json"]/@href').get()
            embedded_json = response.selector.xpath(
                '//script[@type="application/ld+json"]/text()').get()

            if linked_json:
                # follow link to json file and get data
                req = requests.get(linked_json)
                json_obj = json.loads(req.content)

            elif embedded_json:
                # parse json data from html source
                # remove whitespace that is not in a value
                embedded_json = re.sub(r'\s+[^\:\S\"]', "", embedded_json)
                self.json_list.append(json.loads(embedded_json[1:-1]))
            else:
                print(f"No valid JSON-LD data in {response.url}.")
                return

            # append source and date metadata
            json_obj["source"] = response.url
            json_obj["accessed"] = str(datetime.datetime.now())

            # append json_obj to json_list
            self.json_list.append(json_obj)
            print(f"{response.url} successfully scraped.")

        except json.JSONDecodeError:
            print(f"Bad JSON format at {response.url}. Skipping file.")
            return

        # return self.json_list


process = CrawlerProcess(
    # requests throttled due to limitations of python http.server
    # this should not be necessary in production
    settings={
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 10,
        "LOG_LEVEL": "ERROR",
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    }
)

process.crawl(JsonScraper)
process.start()
