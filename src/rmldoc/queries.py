authors = """
PREFIX dc: <http://purl.org/dc/terms/> 
PREFIX schema: <http://schema.org/>
SELECT ?s ?name ?mbox WHERE{
    ?s (dc:contributor|schema:contributor)  foaf:Person;
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
PREFIX dcterms: <http://purl.org/dc/terms/>
SELECT ?version ?license ?description ?title
WHERE {
 VALUES (?map_class) {(schema:Dataset)(void:Dataset)}.
    ?triplesMap a ?map_class.
    OPTIONAL {?triplesMap schema:version ?version.}
    OPTIONAL {?triplesMap schema:license ?license.}
    OPTIONAL {?triplesMap (schema:description| dcterms:description) ?description.}
    OPTIONAL {?triplesMap schema:title ?title.}
    
}
"""