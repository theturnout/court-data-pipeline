import os
from components.csv_import import csv_import
from components.data_importer import data_importer
from scrapy.crawler import CrawlerProcess
from classes.json_scraper import JsonScraper
from classes.validator import Validator
import argparse
from data.dev_data import json_list  # contains expected output of JsonScraper


def main():

    # define argument for providing csv file with urls to be scraped
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "urls", help="A list of website URLs to scrape for JSON-LD data provided in CSV format.")

    # parse url csv path from arg
    args = parser.parse_args()
    url_csv = args.urls

    # check file has .csv extension
    if os.path.splitext(url_csv)[-1] != ".csv":
        print("URLs must be provided in CSV format.")
        return

    # pipeline = csv_import -> JsonScraper -> Validator -> Db_importer -> Db_exporter

    # # import and parse csv
    urls = csv_import(url_csv)

    # crawl provided urls and scrape json-ld data if present
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

    process.crawl(JsonScraper, urls=urls)
    process.start()

    # Validate files

    validated_files = Validator(json_list)
    valid_json = validated_files.validate_json()

    # Import records to DB
    data_importer(valid_json)


if __name__ == "__main__":
    main()
