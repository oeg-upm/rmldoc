authors2 = """
PREFIX dc: <http://purl.org/dc/terms/> 
PREFIX schema: <http://schema.org/>
SELECT ?s ?name ?mbox WHERE{
    ?s (dc:contributor|schema:contributor|schema:author)  foaf:Person;
    OPTIONAL {?s rdfs:label ?name.}
    OPTIONAL {?s foaf:mbox ?mbox.}
}
"""


def authors():
    query = """
    PREFIX dc: <http://purl.org/dc/terms/> 
    PREFIX schema: <http://schema.org/>
    SELECT ?s ?name ?mbox WHERE{
        ?s (dc:contributor|schema:contributor|schema:author)  foaf:Person;
        OPTIONAL {?s rdfs:label ?name.}
        OPTIONAL {?s foaf:mbox ?mbox.}
    }
    """
    return query


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


def dataset_version():
    query = f"""
PREFIX schema: <http://schema.org/>
PREFIX void: <http://rdfs.org/ns/void#>
PREFIX dc: <http://purl.org/dc/terms/>
PREFIX dcat: <http://www.w3.org/ns/dcat#> 

SELECT DISTINCT ?version ?license ?description ?title ?dateCreated
WHERE {{
 VALUES (?map_class) {{(schema:Dataset)(void:Dataset)(dcat:Dataset)}}.
    ?triplesMap a ?map_class.
    OPTIONAL {{?triplesMap (schema:version|dcat:version) ?version.}}
    OPTIONAL {{?triplesMap (schema:license|dc:license) ?license.}}
    OPTIONAL {{?triplesMap (schema:description| dc:description) ?description.}}
    OPTIONAL {{?triplesMap (schema:title|dc:title) ?title.}}
    OPTIONAL {{?triplesMap (schema:dateCreated|dc:created) ?dateCreated.}}
}}
    """
    return query


def logical_source(triples_map):
    query = f"""
    PREFIX  rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX  rml: <http://w3id.org/rml/>
    PREFIX  ns0: <http://semweb.mmlab.be/ns/rml#>
    SELECT ?source ?label ?comment
    WHERE {{
        <{triples_map}> (ns0:logicalSource|rml:logicalSource|rr:logicalTable) ?logicalSource.
        ?logicalSource (ns0:source|rml:source|rr:tableName) ?source.
        OPTIONAL {{?logicalSource rdfs:label ?label }}
        OPTIONAL {{?logicalSource rdfs:comment ?comment. }}
    }}"""
    return query


def subject_map_old(triples_map):
    query = f"""
    PREFIX  rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX  rml: <http://w3id.org/rml/>
    PREFIX  ns0: <http://semweb.mmlab.be/ns/rml#>
    SELECT ?subjectMap ?template ?label ?comment
    WHERE {{
         <{triples_map}> (rr:subjectMap|rml:subjectMap) ?subjectMap.
        ?subjectMap (rr:template|rml:template|ns0:reference) ?template.
        OPTIONAL {{?subjectMap rdfs:label ?label }}
        OPTIONAL {{?subjectMap rdfs:comment ?comment. }}
        #FILTER (!isBlank(?template))
    }}"""
    return query


def subject_map(triples_map):
    query = f"""
    PREFIX rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX rml: <http://w3id.org/rml/>
    PREFIX ns0: <http://semweb.mmlab.be/ns/rml#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?subjectMap ?template ?termType ?label ?comment
    WHERE {{
        <{triples_map}> (rr:subjectMap|rml:subjectMap) ?subjectMap.

        # Obtenemos el template o referencia
        OPTIONAL {{ ?subjectMap (rr:template|rml:template|ns0:reference) ?template. }}

        # Detectamos si es un Blank Node explícito
        OPTIONAL {{ ?subjectMap rr:termType ?termType. }}

        OPTIONAL {{ ?subjectMap rdfs:label ?label. }}
        OPTIONAL {{ ?subjectMap rdfs:comment ?comment. }}
    }}"""
    return query

def predicate_object_map_old(triples_map):
    query = f"""
    PREFIX  rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX  rml: <http://w3id.org/rml/>
    PREFIX  ns0: <http://semweb.mmlab.be/ns/rml#>
    SELECT ?pr_constant ?ob_constant
    WHERE {{

        <{triples_map}>  (rr:predicateObjectMap|rml:predicateObjectMap|ns0:predicateObjectMap) ?predicateObjectMap.
        ?predicateObjectMap (rr:predicateMap|rml:predicateMap|ns0:predicateMap)/(rr:constant|rml:constant|ns0:constant)|(rr:predicate) ?pr_constant.
        ?predicateObjectMap (rr:objectMap|rml:objectMap|ns0:objectMap)/((rr:reference|rml:reference|ns0:reference)|(rr:constant|rml:constant|ns0:constant)|(rr:template|rml:template|ns0:template)) ?ob_constant.

        #OPTIONAL {{ ?predicateObjectMap rdfs:label ?label }}
        #OPTIONAL {{ ?predicateObjectMap rdfs:comment ?comment. }}
    }}
    """
    return query


def predicate_object_map(triples_map):
    query = f"""
    PREFIX rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX rml: <http://w3id.org/rml/>
    PREFIX ns0: <http://semweb.mmlab.be/ns/rml#>

    SELECT ?pr_constant ?ob_value
    WHERE {{
        <{triples_map}> (rr:predicateObjectMap|rml:predicateObjectMap|ns0:predicateObjectMap) ?pom.

        # Predicado: extrae la constante o el predicado directo
        ?pom (rr:predicateMap|rml:predicateMap|ns0:predicateMap) ?pm.
        ?pm (rr:constant|rr:predicate|rml:constant|ns0:constant) ?pr_constant.

        # Objeto: extrae constante, columna o template
        ?pom (rr:objectMap|rml:objectMap|ns0:objectMap) ?om.
        ?om (rr:constant|rr:column|rr:template|rml:reference|rml:constant|rml:template|ns0:reference|ns0:constant|ns0:template) ?ob_value.
    }}
    """
    return query

def named_graph(triples_map):
    query = f"""
    PREFIX  rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX  rml: <http://w3id.org/rml/>
    PREFIX  ns0: <http://semweb.mmlab.be/ns/rml#>
    SELECT distinct ?graph
    WHERE {{
        <{triples_map}> rr:subjectMap/rr:graphMap/rr:constant ?graph .
    }}
     """
    return query


def join_condition(triples_map):
    query = f"""
    PREFIX  rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX  rml: <http://w3id.org/rml/>
    PREFIX  ns0: <http://semweb.mmlab.be/ns/rml#>
    SELECT distinct *
    WHERE {{
        <{triples_map}> rr:predicateObjectMap/rr:objectMap/rr:joinCondition[rr:child ?child; rr:parent ?parent; ^rr:joinCondition/rr:parentTriplesMap ?parentTriplesMap; ^rr:joinCondition/^rr:objectMap/rr:predicateMap/rr:constant ?predicate; ^rr:joinCondition/^rr:objectMap/^rr:predicateObjectMap/rr:subjectMap/rr:template   ?s_template ].
        ?parentTriplesMap rr:subjectMap/(rr:template|ns0:reference) ?o_template.
    }}
    """
    return query


def logical_source_info(triples_map):
    query = f"""
    PREFIX rr: <http://www.w3.org/ns/r2rml#>
    PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

    SELECT DISTINCT ?source ?tableName ?sqlQuery ?iterator ?referenceFormulation
    WHERE {{
        BIND(<{triples_map}> AS ?tm)
        {{
            # Bloque RML: logicalSource
            ?tm rml:logicalSource ?ls .
            OPTIONAL {{ ?ls rml:source ?source . }}
            OPTIONAL {{ ?ls rml:referenceFormulation ?referenceFormulation . }}
            OPTIONAL {{ ?ls rml:iterator ?iterator . }}
            OPTIONAL {{ ?ls rr:sqlQuery ?sql1 . }}
            OPTIONAL {{ ?ls rml:query ?sql2 . }}
            BIND(COALESCE(?sql1, ?sql2) AS ?sqlQuery)
        }} 
        UNION 
        {{
            # Bloque R2RML: logicalTable
            ?tm rr:logicalTable ?lt .
            OPTIONAL {{ ?lt rr:tableName ?tableName . }}
            OPTIONAL {{ ?lt rr:sqlQuery ?sqlQuery . }}
        }}
    }}
    """
    return query


def term_map_info():
    query = f"""
    PREFIX rr: <http://www.w3.org/ns/r2rml#>
    PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

    SELECT DISTINCT ?constant ?template ?reference ?column ?termType
    WHERE {{
      

        OPTIONAL {{ ?map rr:constant ?constant . }}
        OPTIONAL {{ ?map rr:template ?template . }}
        OPTIONAL {{ ?map rml:reference ?reference . }}
        OPTIONAL {{ ?map rr:column ?column . }}
        OPTIONAL {{ ?map rr:termType ?termType . }}
    }}
    """
    return query

def pom_info_query_old(triples_map):
    return f"""
    PREFIX rr: <http://www.w3.org/ns/r2rml#>
    PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

    SELECT DISTINCT ?p ?constant ?template ?reference ?column ?termType ?parentTriplesMap
    WHERE {{
        <{triples_map}> rr:predicateObjectMap ?pom .
        ?pom rr:predicateMap/rr:constant ?p .

        {{
            # Caso 1: ObjectMap normal
            ?pom rr:objectMap ?om .
            OPTIONAL {{ ?om rr:constant ?constant . }}
            OPTIONAL {{ ?om rr:template ?template . }}
            OPTIONAL {{ ?om rml:reference ?reference . }}
            OPTIONAL {{ ?om rr:column ?column . }}
            OPTIONAL {{ ?om rr:termType ?termType . }}
        }}
        UNION
        {{
            # Caso 2: RefObjectMap
            ?pom rr:objectMap ?om .
            ?om rr:parentTriplesMap ?parentTriplesMap .
        }}
    }}
    """
def pom_info_query(triples_map):
    return f"""
    PREFIX rr: <http://www.w3.org/ns/r2rml#>
    PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

    SELECT DISTINCT ?p ?constant ?template ?reference ?column ?termType
    WHERE {{
        <{triples_map}> rr:predicateObjectMap ?pom .
        ?pom rr:predicateMap/rr:constant ?p .

        {{
            ?pom rr:objectMap ?om .
            OPTIONAL {{ ?om rr:constant ?constant . }}
            OPTIONAL {{ ?om rr:template ?template . }}
            OPTIONAL {{ ?om rml:reference ?reference . }}
            OPTIONAL {{ ?om rr:column ?column . }}
            OPTIONAL {{ ?om rr:termType ?termType . }}
        }}
         FILTER (BOUND(?constant) || BOUND(?template) || BOUND(?reference) || BOUND(?column))
    }}
    """