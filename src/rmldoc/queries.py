authors = """
PREFIX dc: <http://purl.org/dc/terms/> 
PREFIX schema: <http://schema.org/>
SELECT ?s ?name ?mbox WHERE{
    ?s (dc:contributor|schema:contributor|schema:author)  foaf:Person;
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
PREFIX schema: <http://schema.org/>
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX dc: <http://purl.org/dc/terms/>
PREFIX dcat: <http://www.w3.org/ns/dcat#> 

SELECT ?version ?license ?description ?title ?dateCreated
WHERE {
 VALUES (?map_class) {(schema:Dataset)(void:Dataset)(dcat:Dataset)}.
    ?triplesMap a ?map_class.
    OPTIONAL {?triplesMap (schema:version|dcat:version) ?version.}
    OPTIONAL {?triplesMap (schema:license|dc:license) ?license.}
    OPTIONAL {?triplesMap (schema:description| dc:description) ?description.}
    OPTIONAL {?triplesMap (schema:title|dc:title) ?title.}
    OPTIONAL {?triplesMap (schema:dateCreated|dc:created) ?dateCreated.}
}
"""