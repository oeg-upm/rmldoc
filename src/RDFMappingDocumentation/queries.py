authors = """
SELECT ?s ?name ?mbox WHERE{
    ?s ?contributor  foaf:Person;
    OPTIONAL {?s rdfs:label ?name.}
    OPTIONAL {?s foaf:mbox ?mbox.}
}
"""

triples_map_query = """
SELECT ?TriplesMap ?label ?comment ?source ?template
WHERE {
    ?TriplesMap a rr:TriplesMap.
    #?TriplesMap rml:logicalSource ?logicalSource.
    #?logicalSource rml:source ?source.
    #?TriplesMap rr:subjectMap ?subjectMap.
    #?subjectMap rr:template ?template.
    OPTIONAL {?TriplesMap rdfs:label ?label }
    OPTIONAL {?TriplesMap rdfs:comment ?comment. }
}"""