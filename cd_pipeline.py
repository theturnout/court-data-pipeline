import scripts.scraper as scraper
import scripts.validator as validator
import scripts.db_importer as db_importer
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

    scraper.main(urls)

    validator.main()

    db_importer.main()


if __name__ == "__main__":
    main()
