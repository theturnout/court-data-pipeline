import os
import glob
from scrapy.crawler import CrawlerProcess
from spiders.JsonSpider import JsonSpider

# SCRAPE WEBPAGES PROVIDED IN CSV #

### dev ###
# clear destination dir
files = glob.glob("/data/raw_json/*")
for file in files:
    os.remove(file)
### /dev ###


def scraper(urls):

    process = CrawlerProcess(
        # requests throttled due to limitations of python http.server
        # this should not be necessary in production
        settings={
            "DOWNLOAD_DELAY": 1,
            "CONCURRENT_REQUESTS_PER_DOMAIN": 10,
            "LOG_LEVEL": "ERROR"
        }
    )

    process.crawl(JsonSpider)
    process.start(stop_after_crawl=False)

    return 1
