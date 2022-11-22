# Court Data Pipeline

## Purpose

The Pew Charitable Trusts' civil legal modernization project seeks to make civil court systems more open, efficient, and equitable by promoting policies, processes, and technologies that can improve outcomes for civil litigants. As part of this effort, a data standard and storage format are being developed in partnership with court administrators and information technology specialists to make courthouse information more accessible to the public via internet search engines.

## Overview

The tool scrapes JSON-LD data from court websites, validates it against a SHACL schema, and stores the linked data as triples in a database. Web scraping is done using Scrapy, validation with pyshacl, and storage with SQLAlchemy and sqlite. The standard vocabulary is provided by Schema.org and is supplemented with extensions developed for this project.

## Requirements
- Python >= 3.10
- pipenv >= 2022.10.11


## Setting Up the Environment

1. Create a virtual environment with `pipenv` and install dependencies by executing the following commands in a terminal or command prompt window.
   
  `pipenv sync`  
  `pipenv shell`
  
2. Create a `.env` file and define a variable that indicates the location in which the database will be stored. The file should contain the following.

```
DB_LOC = "/path/to/database_dir/"
``` 
  
## Running the Script
1. Start a local server. It will serve the contents of the current directory on Port 8000. The contents of the definition files are accessed via HTTP so validation will fail if they cannot be reached.
  
`pipenv run python -m http.server`


2. Webpages to be scraped are provided to the script by passing a CSV file as an argument when executing the `.py` file. The location of the CSV file does not matter as long as the path in the argument is valid. Execute the following command to run the script.

`pipenv run python scraper.py "./data/sites/websites.csv"`


3. Execute the validation script with the following command.

`pipenv run python validator.py`


4. Import the validated JSON files with the following command.

`pipenv run python db-importer.py`

For development purposes, a Jupyter Notebook is also included in the repo. **This is for development only** and the `.py` scripts should be used as the default methods of interacting with the pipeline. While all files should be kept in parity, the `.py` scripts always supersede the notebook. 

The `.ipynb` file is located in the `scripts/` directory. To view the notebook, start a Jupyter server with the commands below and navigate to localhost in a browser window. This should be done within the virtual environment.

`jupyter lab`  
or  
`jupyter notebook`
