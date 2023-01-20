import os
from dotenv import load_dotenv
from rdflib.graph import Graph


def data_importer(valid_json):
    """
    Import validated JSON-LD data into RDF datastore
    """

    # load environmental variables
    load_dotenv()
    DB = os.getenv("DB_LOC") + "/court-data.db"

    if len(valid_json) < 1:
        print("No files provided to importer. Exiting script.")
        raise SystemExit

    # configure dialect/engine
    graph = Graph(store='Oxigraph', identifier='http://court')

    print(f"Starting DB import with {len(valid_json)} files.")

    # connect to db
    # 'create' arg should only be true the first time
    # the importer is run. It will overwrite the db
    # file otherwise.
    graph.open(DB, create=True)

    file_count = 0

    for file in valid_json:
        graph.parse(data=file, format="json-ld")
        file_count += 1

    graph.close()

    print(f"{file_count} files successfully imported to DB.\nExecute 'queries/run_query.py' to export database contents to 'queries/results'.\nSee README for more information.\nScript finished.\n")
