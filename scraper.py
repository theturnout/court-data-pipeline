import sys
import os
import regex as re
import json
import csv
import requests
import datetime
import glob
import scrapy
from scrapy.crawler import CrawlerProcess

# SCRAPE WEBPAGES PROVIDED IN CSV #

### dev ###
# clear destination dir
files = glob.glob("/data/raw_json/*")
for file in files:
    os.remove(file)

# use local files
# dev_sites = glob.glob("data/sites/*/*.html")
### /dev ###


# list of sites to scrape
# sites = dev_sites

class JsonSpider(scrapy.Spider):
    
    """ 
    scrape .json-ld data from court websites.
    prefer linked .json, 
    scrape embedded data otherwise.
    """

    name = "court-data-spider"
    

    def start_requests(self):
          
        # load sites from csv provided as argument
        urls = sys.argv[1]
        sites = []

        with open("data/sites/websites.csv", 'r') as f:
            reader = csv.reader(f)
            sites = [el for sub in list(reader) for el in sub]

        # GET request, pass res to parse()
        for url in sites:
            yield scrapy.Request(url=f"http://localhost:8000/{url}", callback=self.parse)

            
    def parse(self, response):

        # look for json data. 
        linked_json = response.selector.xpath(
            '//link[@type="application/ld+json"]/@href').get()
        embedded_json = response.selector.xpath(
            '//script[@type="application/ld+json"]/text()').get()

        # use page source as filename, replace "/"
        # need a better convention
        page_source = response.url.replace("/", ".")
        filename = (page_source + ".json").replace(".html","")
  
        if linked_json is not None:
            # follow link to json file and grab data
            req = requests.get(linked_json)
            # to append source and date metadata below
            load_json = json.loads(req.content)        
        elif embedded_json is not None:
            # parse json data from html source
            # remove whitespace that is not in a value
            embedded_json = re.sub(r'\s+[^\:\S\"]', "", embedded_json)  
            # to append source and date metadata below
            load_json = json.loads(embedded_json[1:-1])
        else:
            return f"No valid JSON-LD data in {response.url}."

        # append source and date metadata
        load_json.append(
            {"source": response.url, "accessed": str(datetime.datetime.now())})

        # write json file
        json_out = json.dumps(load_json)
        with open(f"./data/raw_json/{filename}", "w") as output:
            output.write(json_out)

process = CrawlerProcess(
    # requests throttled due to limitations of python http.server
    # this should not be necessary in production
    settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 10
    }
)

process.crawl(JsonSpider)
process.start()