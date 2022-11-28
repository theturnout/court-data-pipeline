from scripts.scraper import scraper
from scripts.validator import validate_json
from scripts.db_importer import db_importer
import argparse


def main():

    # if args.urls[-3:-1] != ".csv":
    #     print("URLs must be provided in CSV format.")
    #     return

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "urls", help="A list of website URLs to scrape for JSON-LD data provided in CSV format.")
    args = parser.parse_args()
    urls = scraper(args.urls)

    if scraper(urls) == 1:
        print("scraper script executed successfully.")
        validate_json()
        if validate_json() == 1:
            print("validate_json script executed successfully.")
            if db_importer() == 1:
                print("db_importer script executed successfully.")
                print("All pipeline scripts executed successfully.")
                return
            else:
                print("db_importer script failed to execute successfully.")
                return
        else:
            print("validate_json script failed to execute successfully.")
            return
    else:
        print("scraper script failed to execute successfully.")


if __name__ == "__main__":
    main()
