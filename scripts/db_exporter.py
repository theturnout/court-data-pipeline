"""
Imports validated JSON-LD data into an RDF datastore.
"""

import os
import glob
from dotenv import load_dotenv
from rdflib.graph import Graph
from rdflib.store import Store
from rdflib import plugin, Namespace
from rdflib.compare import to_isomorphic, graph_diff

import logging

def main():
    """
    Script to export validated JSON-LD data out of a RDF store.
    """
    # load environmental variables
    load_dotenv()
    DB = os.getenv("DB_LOC") + "court-data.db"

    graph = Graph(store='Oxigraph', identifier='http://court')
    # connect to db
    graph.open(DB)

    with open('../queries/more_advanced.sparql') as qf:
        qt = qf.read()
    qr = graph.query(qt)
    
    to_isomorphic(qr).serialize('../data/query_result.json', format='json-ld')
        
    graph.close()

    return 1


if __name__ == "__main__":
    main()
