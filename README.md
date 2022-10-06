# court-data-scraper

A tool to be used to scrape linked or embedded JSON-LD data from court websites.

## Setting up the environment

1. Create a virtual environment with `pipenv` and install dependencies
  
  `pipenv shell`  
  `pipenv sync`
  
  
2. Start local server. It will serve the contents of the current directory on Port 8000.
  
  `python3 simple_server_cors.py`  
  or  
  `python simple_server_cors.py`
  
  
3. In a terminal window, execute the following command to run the scraper. Code for the scraper can be found in `/court_data_scrapy/spiders/court_data_spider.py`:

	`scrapy crawl court-data-spider`

  
If a message is displayed indicating that a module listed in the Pipfile is not installed, reinstall the modules
  `pipenv uninstall --all`  
  `pipenv install`
# pew-court-data-pipeline
