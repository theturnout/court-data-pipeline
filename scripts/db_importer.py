"""
Imports validated JSON-LD data into an RDF datastore.
"""

import os
import sys
import glob
from dotenv import load_dotenv
from rdflib.graph import Graph
from rdflib.store import Store
from rdflib import plugin


def db_importer():
    """
    Script to import validated JSON-LD data into an RDF store.
    """
    # load environmental variables
    load_dotenv()
    DB = os.getenv("DB_LOC") + "court-data.db"

    ### dev ###
    if os.path.exists(DB):
        os.remove(DB)
    ### dev ###

    # collect all JSON files in valid_json dir
    # valid_json_files = glob.glob("data/valid_json/*.json")
    valid_json_files = glob.glob("../data/raw_json/*.json")

    # configure db connection string
    # this does not have to be sqlite
    # mySQL and postgres are also supported
    conn = f"sqlite:///{DB}"

    # configure dialect/engine
    store = plugin.get("SQLAlchemy", Store)(identifier="court_data_store")
    graph = Graph("SQLAlchemy", identifier='court_data_graph')

    # connect to db
    graph.open(conn, create=True)

    # parse and import data from collected JSON files
    for file in valid_json_files:
        graph.parse(file, format="json-ld")

    # testing #
    result = graph.query("select * where {?s ?p ?o}")

    for subject, predicate, object_ in result:
        print(subject, predicate, object_)
    # /testing #

    graph.close()

    return 1
