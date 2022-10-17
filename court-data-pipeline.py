import glob
import os
import regex as re
import json
import requests
import datetime
from dotenv import load_dotenv
import scrapy
from scrapy.crawler import CrawlerProcess
from pyshacl import validate
from rdflib import plugin
from rdflib.graph import Graph
from rdflib.store import Store
from rdflib_sqlalchemy import registerplugins
import sqlite3

# load environmental variables
load_dotenv()
DB = os.getenv("DB_LOC") + "court-data.db"

# SCRAPE PROVIDED WEBPAGES #

### dev ###
# clear destination dir
files = glob.glob("/data/raw_json/*")
for file in files:
    os.remove(file)

# use local files
dev_sites = glob.glob("data/sites/*/*.html")
### /dev ###


# list of sites to scrape
sites = dev_sites

class JsonSpider(scrapy.Spider):
    
    """ 
    scrape .json-ld data from court websites.
    prefer linked .json, 
    scrape embedded data otherwise.
    """

    name = "court-data-spider"

    def start_requests(self):
          
        global sites
        
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


# VALIDATE SCRAPED DATA #

### dev ### 
# clear destination dir
files = glob.glob("data/valid_json/*")
for file in files:
    os.remove(file)    
### /dev ###


# scraped JSON-LD files 
scraped_json_files = glob.glob("data/raw_json/*")

# SHACL file to validate data against
shacl_file = 'data/defs/court-data-standard-shacl.ttl'

errors = []

def validate_json(scraped_json_files, shacl_file):
    """
    validate scraped json files
    if valid, move to valid_json folder
    if not, append error msg to errors
    """

    for file in scraped_json_files:
        if len(scraped_json_files) < 1:
            print("No files provided. Validation aborted.")
            break
        try:
            r = validate(file,
                         shacl_graph=shacl_file,
                         inference='none',
                         abort_on_first=True,
                         allow_infos=False,
                         allow_warnings=False,
                         meta_shacl=False,
                         advanced=True,
                         js=False,
                         debug=False)
            
            # if error, append msg to errors list
            if r[0] != True:
                msg = r[2]
                errors.append(f"{file}\n{msg}\n")
                print(f"{file} failed validation.")
            # otherwise, move file to valid_json folder
            else:
                renamed_file = str(file.split(".")[-2] + ".json")
                file.replace(".data/raw_json/","")
                os.rename(f"{file}", f"./data/valid_json/{renamed_file}")
                print(f"{file} successfully validated.")
                
        except json.JSONDecodeError:
            errors.append(f"{file}\nBad JSON format. Validation aborted.")
            pass
    
    print(*errors, sep="\n") if errors else print("All files successfully validated.")

validate_json(scraped_json_files, shacl_file)


# IMPORT GRAPHS INTO DATASTORE #

### dev ###
if os.path.exists(DB):
    os.remove(DB)
### dev ###    


valid_json_files = glob.glob("data/valid_json/*.json")
conn =f"sqlite:///{DB}"

graph = Graph("SQLAlchemy", identifier='court_data')
graph.open(conn, create=True)

for file in valid_json_files: 
    graph.parse(file, format="json-ld")

result = graph.query("select * where {?s ?p ?o}")

for subject, predicate, object_ in result:
    print(subject, predicate, object_)

graph.close()