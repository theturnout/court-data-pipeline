import os
import glob
from dotenv import load_dotenv
from rdflib.graph import Graph
import sqlite3

# IMPORT GRAPHS INTO DATASTORE #


def db_importer():
    """
    Import validated JSON-LD data in RDF datastore
    """
    # load environmental variables
    load_dotenv()
    DB = os.getenv("DB_LOC") + "court-data.db"
<<<<<<< HEAD

    valid_json_files = glob.glob("data/valid_json/*.json")
=======
    
    ### dev ###
>>>>>>> ac9475f8aa4d25717110585ec011f6e2e0016d42

    if len(valid_json_files) == 0:
        print("No files provided to importers. Exiting script.")
        return

<<<<<<< HEAD
    conn = f"sqlite:///{DB}"

    graph = Graph("SQLAlchemy", identifier='court_data')
    graph.open(conn, create=True)
=======
    # configure dialect/engine
    graph = Graph(store='Oxigraph', identifier='http://court')

    # connect to db
    graph.open(DB, create=True)
>>>>>>> ac9475f8aa4d25717110585ec011f6e2e0016d42

    for file in valid_json_files:
        graph.parse(file, format="json-ld")

<<<<<<< HEAD
    # Testing, return all records
    # result = graph.query("select * where {?s ?p ?o}")
    # for subject, predicate, object_ in result:
    #     print(subject, predicate, object_)
=======
    # testing #
    result = graph.query("select * where {?s ?p ?o}")
    for subject, predicate, object_ in result:
        print(subject, predicate, object_)
    # /testing #
>>>>>>> ac9475f8aa4d25717110585ec011f6e2e0016d42

    graph.close()

    print("Files successfully imported to DB.\nExecute 'scripts/db_exporter.py' to export database contents to JSON-LD file.\n")
