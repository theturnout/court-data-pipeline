import os
import glob
from dotenv import load_dotenv
from rdflib.graph import Graph
import sqlite3

# IMPORT GRAPHS INTO DATASTORE #

# load environmental variables
load_dotenv()
DB = os.getenv("DB_LOC") + "court-data.db"

### dev ###
if os.path.exists(DB):
    os.remove(DB)
### dev ###    

valid_json_files = glob.glob("data/valid_json/*.json")
conn =f"sqlite:///{DB}"

graph = Graph("SQLAlchemy", identifier='court_data')
graph.open(conn, create=True)

for file in valid_json_files: 
    graph.parse(file, format="json-ld")

result = graph.query("select * where {?s ?p ?o}")

# Testing, return all records
for subject, predicate, object_ in result:
    print(subject, predicate, object_)

graph.close()