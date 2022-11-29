from rdflib.graph import Graph
from rdflib.compare import to_isomorphic, graph_diff
#from rdflib.tools.rdf2dot import rdf2dot
#tests if SPARQL query extract RDF ingested and represented by various files

graph = Graph()
graph.parse('data/dev_data/dev_court_data_3.json')
qt = ""
with open('./queries/more_advanced.sparql') as qf:
    qt = qf.read()
qr = graph.query(qt)
i1 = to_isomorphic(graph)
#with open('mydot.dot','w') as df:
#    rdf2dot(graph, df)
i2 = to_isomorphic(qr)

i1.serialize('i1.ttl')
i2.serialize('i2.ttl')

if i1 != i2:
    in_both, in_first, in_second = graph_diff(i1, i2)
    def dump_nt_sorted(g):
        for l in sorted(g.serialize(format='nt').splitlines()):
            if l: print(l)
    #dump_nt_sorted(in_both) 
    print('⬅️ only in i1')
    dump_nt_sorted(in_first) 
    print('➡️ only in i2')
    dump_nt_sorted(in_second) 
else: 
    print('query is isomorphicly equal to original input')    
    