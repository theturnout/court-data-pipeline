#from xml.dom.xmlbuilder import _DOMInputSourceStringDataType
from pyshacl import validate

'''
script to validate json-ld files
'''

data_graph = './example-court-data.json'
sg = './court-data-standard-shacl.ttl'

r = validate(data_graph,
             shacl_graph=sg,
             #             ont_graph=og,
             inference='none',
             abort_on_first=False,
             allow_infos=True,
             allow_warnings=True,
             meta_shacl=False,
             advanced=True,
             js=False,
             debug=False)
results_text = r

print(r)
