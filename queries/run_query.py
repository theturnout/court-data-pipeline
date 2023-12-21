"""
Exports validated JSON-LD data from an RDF datastore.
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from rdflib.graph import Graph
from rdflib.store import Store
from rdflib import plugin, Namespace
from rdflib.compare import to_isomorphic, graph_diff


def main():
    """
    Script to export validated JSON-LD data out of a RDF store.
    """

    # Define location to which results json will be saved from arg. Defaults to ./results/ if no
    # argument provided.
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--loc",
            help='The location to which the query results are saved. Defaults to "./results/"',
            default="queries/results/",
            dest="results_path",
            nargs="?",
        )

        args = parser.parse_args()
        return args.results_path

    # load environmental variables
    load_dotenv()
    DB = os.getenv("DB_LOC") + "/court-data.db"

    graph = Graph(store="Oxigraph", identifier="http://court")
    # connect to db
    graph.open(DB)

    # load query
    with open("./queries/all_records.sparql") as qf:
        qt = qf.read()

    qr = graph.query(qt)

    results_path = parse_args()
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    to_isomorphic(qr).serialize(f"{results_path}/query_result.json", format="json-ld")
    print(f"Query complete. Check {results_path}/query_result.json for results.\n")

    graph.close()


if __name__ == "__main__":
    main()
