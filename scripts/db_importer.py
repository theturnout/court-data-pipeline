import os
import glob
from dotenv import load_dotenv
from rdflib.graph import Graph

# IMPORT GRAPHS INTO DATASTORE #


def db_importer():
    """
    Import validated JSON-LD data in RDF datastore
    """
    # load environmental variables
    load_dotenv()
    DB = os.getenv("DB_LOC") + "court-data.db"

    valid_json_files = glob.glob("data/valid_json/*.json")

    if len(valid_json_files) == 0:
        print("No files provided to importer. Exiting script.")
        return

    # configure dialect/engine
    graph = Graph(store='Oxigraph', identifier='http://court')

    # connect to db
    graph.open(DB, create=True)

    for file in valid_json_files:
        graph.parse(file, format="json-ld")

    # Testing, return all records
    # result = graph.query("select * where {?s ?p ?o}")
    # for subject, predicate, object_ in result:
    #     print(subject, predicate, object_)

    graph.close()

    print("Files successfully imported to DB.\nExecute 'scripts/db_exporter.py' to export database contents to JSON-LD file.\n")
