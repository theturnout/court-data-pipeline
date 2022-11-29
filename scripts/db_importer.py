"""
Imports validated JSON-LD data into an RDF datastore.
"""

import os
import glob
from dotenv import load_dotenv
from rdflib.graph import Graph
from rdflib.store import Store
from rdflib import plugin


def main():
    """
    Script to import validated JSON-LD data into an RDF store.
    """
    # load environmental variables
    load_dotenv()
    DB = os.getenv("DB_LOC") + "court-data.db"
    
    ### dev ###

    # collect all JSON files in valid_json dir
    # valid_json_files = glob.glob("data/valid_json/*.json")
    valid_json_files = glob.glob("../data/raw_json/*.json")

    # configure dialect/engine
    graph = Graph(store='Oxigraph', identifier='http://court')

    # connect to db
    graph.open(DB, create=True)

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


if __name__ == "__main__":
    main()
