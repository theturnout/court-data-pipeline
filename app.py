import os
from components.csv_import import csv_import
from components.data_importer import data_importer
from scrapy.crawler import CrawlerProcess
from classes.json_scraper import JsonScraper
from classes.validator import Validator
import argparse
from data.dev_data import json_list  # contains expected output of JsonScraper


class App():

    def __init__(self):
        self.url_csv = ""
        self.urls = []
        self.valid_json = []

    def get_args(self):
        # define argument for providing csv file with urls to be scraped
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "urls", help="A list of website URLs to scrape for JSON-LD data provided in CSV format.")

        # parse url csv path from arg
        args = parser.parse_args()
        self.url_csv = args.urls

    def import_csv(self):
        # check file has .csv extension
        if os.path.splitext(self.url_csv)[-1] != ".csv":
            print("URLs must be provided in CSV format.")
            raise SystemExit

        # import and parse csv
        self.urls = csv_import(self.url_csv)

    def scrape_urls(self):
        # crawl provided urls and scrape json-ld data if present
        scraper = JsonScraper([])
        process = CrawlerProcess(scraper.settings)

        process.crawl(JsonScraper, self.urls)
        process.start()

    # Validate files
    def validate_files(self):
        validated_files = Validator(json_list)
        self.valid_json = validated_files.validate_json()

    # Import records to DB
    def import_data(self):
        data_importer(self.valid_json)

    def start_app(self):
        self.get_args()
        self.import_csv()
        self.scrape_urls()
        self.validate_files()
        self.import_data()


if __name__ == "__main__":
    app = App()
    app.start_app()
