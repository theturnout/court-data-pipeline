# Court Data Pipeline

## Purpose

The Pew Charitable Trusts' civil legal modernization project seeks to make civil court systems more open, efficient, and equitable by promoting policies, processes, and technologies that can improve outcomes for civil litigants. As part of this effort, a data standard and storage format are being developed in partnership with court administrators and information technology specialists to make courthouse information more accessible to the public via internet search engines.

## Overview

The tool scrapes JSON-LD data from court websites, validates it against a SHACL schema, and stores the linked data as triples in a database. Web scraping is done using **Scrapy**, validation with **pyshacl**, and storage with **oxrdflib**. The standard vocabulary is provided by [Schema.org](https://schema.org) and is supplemented with extensions developed for this project.

This version of the tool will ingest URLs from a CSV and scrape JSON-LD data (if present) from the provided websites. Any JSON-LD data found is validated against a [SHACL](https://www.w3.org/TR/shacl/) file before being stored in an [RDF](https://www.w3.org/RDF/) triplestore.

This version of the tool will ingest URLs from a CSV and scrape the websites they identify for JSON-LD data. If found, the data will be validated before being stored in an RDF triplestore. Imported data can be retrieved in JSON format by running `db_exporter.py` located in the `scripts` folder.

## Requirements

- Python >= 3.10
- pipenv >= 2022.10.11

## Setting Up the Environment

1. Create a virtual environment with `pipenv` and install dependencies by executing the following commands in a terminal or command prompt window.

```bash
pipenv sync
pipenv shell
```

2. Create a `.env` file in the root directory and define a variable that indicates the location in which the database will be stored. The file should contain the following:

```text
DB_LOC = "absolute/path/to/database"
```

## Running the Script

1. Start a local server. It will serve the contents of the current directory on Port 8000. The contents of the definition files (under `data/defs`) are accessed via HTTP so validation will fail if they cannot be reached.

> Note: these resources are now available online and should obviate the need to host them locally. The current version still requires local hosting and so this step is still necessary. It will be removed in a later version.

`python -m http.server`

2. Webpages to be scraped are provided to the script by passing a CSV file as an argument when executing the `.py` file. The location of the CSV file does not matter as long as the path in the argument is valid. Execute the following command to run the script with sample data.

`python app.py data/sites/websites.csv`

3. The pipeline terminates after storing the data ingested by the web scraper in an RDF data store. Queries against the database must be done using [SPARQL](https://www.w3.org/TR/sparql11-query/). Examples of simple queries are included in the `queries` directory and can be run by executing the `run_query.py` script. By default, the script will return all records. In `run_query.py`, change the path in the `open` statement on Line 26 to `queries/basic.sparql` or `queries/more_advanced.sparql` to return other examples of data stored by the pipeline.
