import scrapy
import glob
import os
import regex as re
import json
import requests
import datetime


class JsonSpider(scrapy.Spider):
    """ 
    scrape .json-ld data from court websites.
    prefer linked .json, scrape embedded data otherwise,
    return msg if no data found.
    """

    name = "court-data-spider"

    def start_requests(self):
        # list of sites to scrape
        site_list = []
        all_sites = glob.glob("sites/*/*.html")
        
        # for dev, use local files
        site_list  = all_sites
        # GET request
        for url in site_list:
            yield scrapy.Request(url=f"http://localhost:8000/{url}", callback=self.parse)

    def parse(self, response):

        # look for json data. 
        # prefer linked json file,
        # otherwise parse embedded data
        linked_json = response.selector.xpath(
            '//link[@type="application/ld+json"]/@href').get()
        embedded_json = response.selector.xpath(
            '//script[@type="application/ld+json"]/text()').get()

        # use page source as filename, replace "/"
        page_source = response.url.replace("/", ".")

        # follow link to json file and grab data
        if linked_json is not None:
            req = requests.get(linked_json)
            filename = page_source + ".json"       # need a convention

            # append source and date metadata
            load_json = json.loads(req.content)
            load_json.append(
                {"source": page_source, "accessed": str(datetime.datetime.now())})
            json_out = json.dumps(load_json)
            with open(f"raw_json/{filename}", "w") as output:
                output.write(json_out)

        # extract embedded json data.
        # remove whitespace that is not in a value
        elif embedded_json is not None:
            embedded_json = re.sub(r'\s+[^\:\S\"]', "", embedded_json)
            filename = page_source + ".json"     # need a convention
            load_json = json.loads(embedded_json[1:-1])

            # append source and date metadata
            load_json.append(
                {"source": page_source, "accessed": str(datetime.datetime.now())})
            json_out = json.dumps(load_json)
            with open(f"raw_json/{filename}", "w") as output:
                output.write(json_out)

        # for debug, output blank file if no data found
        else:
            with open(f"output/{page_source}", "w") as output:
                output.write("no data found")