authors = """
prefix dc: <http://purl.org/dc/terms/> 
SELECT ?s ?name ?mbox WHERE{
    ?s dc:contributor  foaf:Person;
    OPTIONAL {?s rdfs:label ?name.}
    OPTIONAL {?s foaf:mbox ?mbox.}
}
"""

triples_map_query = """
PREFIX  rr: <http://www.w3.org/ns/r2rml#> 
PREFIX  rml: <http://w3id.org/rml/>

SELECT ?triplesMap ?label ?comment
WHERE {
    ?triplesMap a ?TriplesMapClass.
    OPTIONAL {?triplesMap rdfs:label ?label }
    OPTIONAL {?triplesMap rdfs:comment ?comment. }
    FILTER (?TriplesMapClass IN (rml:TriplesMap, rr:TriplesMap))
}
"""

dataset_version = """

PREFIX dcat: <http://www.w3.org/ns/dcat#>
SELECT ?version
WHERE {
    ?triplesMap a dcat:Dataset;
    dcat:version ?version.
}
"""