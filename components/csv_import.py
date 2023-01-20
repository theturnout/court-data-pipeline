"""
Ingests a CSV file with one URL per row
and creates a list of URLs to be used by
the JsonScraper class.
"""

import csv


def csv_import(url_csv):

    # read .csv, generate list of urls from rows
    with open(url_csv, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        urls = [url for row in list(reader) for url in row]

    # stop if provided file is empty
    if len(urls) == 0:
        print("No URLs found in file.")
        return
    else:
        return urls
