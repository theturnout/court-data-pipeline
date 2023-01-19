from scrapy.crawler import CrawlerProcess
# from spiders.JsonSpider import JsonSpider
import regex as re
import os
import json
import csv
import requests
import datetime
import scrapy


class JsonScraper(scrapy.Spider):

    name = "court_data_spider"

    def __init__(self, urls, *args, **kwargs):
        super(JsonScraper, self).__init__(*args, **kwargs)
        self.urls = urls
        self.json_list = []
        self.settings = {
            # DOWNLOAD_DELAY is required due to limitations of http.server.
            # It should not be necessary when accessing remote urls.
            "DOWNLOAD_DELAY": 1,
            "CONCURRENT_REQUESTS_PER_DOMAIN": 10,
            "LOG_LEVEL": "ERROR",
            "DOWNLOAD_HANDLERS": {
                "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
                "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            },
            "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
        }

    def start_requests(self):

        if len(self.urls) < 1:
            print("No URLs provided to scraper. Exiting.")
            raise SystemExit

        print(f"Starting web scraper with {len(self.urls)} URLs.")

        # GET request, pass response to parse()
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):

        # try:
        # look for json data.
        linked_json = response.selector.xpath(
            '//link[@type="application/ld+json"]/@href').get()
        embedded_json = response.selector.xpath(
            '//script[@type="application/ld+json"]/text()').get()

        # # use page source as filename, append ".json"
        filename = os.path.splitext(response.url)[0] + ".json"
        filename = filename.split("/")[-1]

        if linked_json is not None:
            # follow link to json file and grab data
            res = requests.get(linked_json)
            load_json = json.loads(res.content)
        elif embedded_json is not None:
            # parse json data from html source
            # remove whitespace that is not in a value
            load_json = re.sub(r'\s+[^\:\S\"]', "", embedded_json)
            load_json = json.loads(load_json[1:-1])
        else:
            print(f"No valid JSON-LD data in {response.url}.")
            return

        # append source and date metadata
        load_json["source"] = response.url
        load_json["accessed"] = str(datetime.datetime.now())

        # self.json_list.append(load_json)
        # print(f"{response.url} successfully scraped.")
        # return

        # write json file
        json_out = json.dumps(load_json)
        with open(f"./data/json/scraped/{filename}", "w") as output:
            output.write(json_out)
        print(f"{response.url} successfully scraped.")

        # except json.JSONDecodeError:
        #     print("Bad JSON format. Skipping file.")
        #     return
