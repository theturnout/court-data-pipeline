from scrapy.crawler import CrawlerProcess
# from spiders.JsonSpider import JsonSpider
import regex as re
import json
import csv
import requests
import datetime
import scrapy


def scraper(urls):
    """
    scrape .json-ld data from court websites.
    prefer linked .json,
    scrape embedded data otherwise.
    """

    class JsonSpider(scrapy.Spider):

        name = "court-data-spider"

        def start_requests(self):

            # load sites from csv provided by argparse
            url_csv = urls

            sites = []

            with open(url_csv, 'r') as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header
                sites = [el for sub in list(reader) for el in sub]

            if len(sites) == 0:
                print("No URLs provided.")
                return

            print("Starting web scraper.")

            # GET request, pass res to parse()
            for url in sites:
                yield scrapy.Request(url, callback=self.parse)

        def parse(self, response):

            try:
                # look for json data.
                linked_json = response.selector.xpath(
                    '//link[@type="application/ld+json"]/@href').get()
                embedded_json = response.selector.xpath(
                    '//script[@type="application/ld+json"]/text()').get()

                # use page source as filename, replace "/"
                page_source = response.url.replace("/", ".")
                filename = (page_source + ".json").replace(".html", "")

                if linked_json is not None:
                    # follow link to json file and grab data
                    req = requests.get(linked_json)
                    load_json = json.loads(req.content)
                elif embedded_json is not None:
                    # parse json data from html source
                    # remove whitespace that is not in a value
                    embedded_json = re.sub(r'\s+[^\:\S\"]', "", embedded_json)
                    load_json = json.loads(embedded_json[1:-1])
                else:
                    print(f"No valid JSON-LD data in {response.url}.")
                    return

                # append source and date metadata
                load_json["source"] = response.url
                load_json["accessed"] = str(datetime.datetime.now())

                # write json file
                json_out = json.dumps(load_json)
                with open(f"./data/raw_json/{filename}", "w") as output:
                    output.write(json_out)

                print(f"{response.url} successfully scraped.")
            except json.JSONDecodeError:
                print("Bad JSON format. Skipping file.")
                return

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

    process.crawl(JsonSpider)
    process.start()
