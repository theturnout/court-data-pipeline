import os
from components.csv_import import csv_import
from classes.JsonScraper import JsonScraper
from classes.validator import Validator
# import classes.db_importer

import argparse


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

    # import and parse csv
    urls = csv_import(url_csv)

    # crawl provided urls and scrape json-ld data if present
    scraper = JsonScraper(urls)

    json_list = scraper.start_requests()

    # scripts.validator.validator()

    Validator.validate(json_list)

    # scripts.db_importer.db_importer()


if __name__ == "__main__":
    main()
