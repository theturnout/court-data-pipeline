import scripts.scraper
import scripts.validator
import scripts.db_importer
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "urls", help="A list of website URLs to scrape for JSON-LD data provided in CSV format.")
    args = parser.parse_args()
    urls = args.urls

    if urls[-4::] != ".csv":
        print("URLs must be provided in CSV format.")
        return

    scripts.scraper.scraper(urls)

    scripts.validator.validator()

    scripts.db_importer.db_importer()


if __name__ == "__main__":
    main()
