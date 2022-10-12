# Court Data Pipeline

## Purpose

The Pew Charitable Trusts' civil legal modernization project seeks to make civil court systems more open, efficient, and equitable by promoting policies, processes, and technologies that can improve outcomes for civil litigants. As part of this effort, a data standard and storage format are being developed in partnership with court administrators and information technology specialists to make courthouse information more accessible to the public via internet search engines.

## Overview

The tool scrapes JSON-LD data from court websites, validates it against a SHACL schema, and stores the linked data as triples in a database. Web scraping is done using Scrapy, validation with pyshacl, and storage with SQLAlchemy and sqlite. The standard vocabulary is provided by Schema.org and is supplemented with extensions developed for this project.

## Requirements
- Python >= 3.10
- pipenv >= 2022.10.11


## Setting up the environment

1. Create a virtual environment with `pipenv` and install dependencies
  
  `pipenv shell`  
  `pipenv sync`
  
  
2. Start local server. It will serve the contents of the current directory on Port 8000.
  
  `pipenv run python simple_server_cors.py`  
  or  
  `pipenv run python simple_server_cors.py`
  
  
3. In a terminal window, execute the following command to run the script:

	`pipenv run python court-data-pipeline.py`


For development purposes, a Jupyter Notebook is also included in the repo. Start the Jupyter server and navigate to localhost in a browser window.

`jupyter lab`  
or  
`jupyter notebook`
