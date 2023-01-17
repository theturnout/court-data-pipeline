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
        return

    # configure dialect/engine
    graph = Graph(store='Oxigraph', identifier='http://court')

    # connect to db
    # 'create' arg should only be true the first time
    # the importer is run. It will overwrite the db
    # file otherwise.
    graph.open(DB, create=True)

    for file in valid_json:
        graph.parse(data=file, format="json-ld")

    # Testing, return all records
    # result = graph.query("select * where {?s ?p ?o}")
    # for subject, predicate, object_ in result:
    #     print(subject, predicate, object_)

    graph.close()

    print("Files successfully imported to DB.\nExecute 'components/db_exporter.py' to export database contents to JSON-LD file.\n")
