# =============================================================================
# queries.py
#
# SPARQL query builders for the rmldoc pipeline.
#
# Each function accepts a triples-map URI (or no arguments for generic
# queries) and returns a ready-to-execute SPARQL SELECT string.
#
# Naming conventions used throughout:
#   rr   – R2RML  (http://www.w3.org/ns/r2rml#)
#   rml  – RML    (http://w3id.org/rml/ or http://semweb.mmlab.be/ns/rml#)
#   ns0  – legacy RML prefix (http://semweb.mmlab.be/ns/rml#)
#
# Functions marked with the suffix ``_old`` are kept for reference only
# and are not called by the current pipeline.
# =============================================================================


# -----------------------------------------------------------------------------
# Author / contributor queries
# -----------------------------------------------------------------------------

# Unused module-level string variant — superseded by the authors() function below.
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
    """
    Return a SPARQL query that retrieves contributors / authors declared on
    the dataset node using dc:contributor, schema:contributor, or
    schema:author.

    Binds:
        ?s     – the contributor / author node
        ?name  – rdfs:label of the person (optional)
        ?mbox  – foaf:mbox address (optional)
    """
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


# -----------------------------------------------------------------------------
# Triples-map discovery
# -----------------------------------------------------------------------------

# Module-level constant — used directly (not called as a function) by the
# processor to enumerate all rr:TriplesMap / rml:TriplesMap instances.
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


# -----------------------------------------------------------------------------
# Dataset metadata
# -----------------------------------------------------------------------------

def dataset_version():
    """
    Return a SPARQL query that extracts top-level dataset metadata from nodes
    typed as schema:Dataset, void:Dataset, or dcat:Dataset.

    Binds:
        ?version      – version string
        ?license      – license URI
        ?description  – free-text description
        ?title        – dataset title
        ?dateCreated  – creation date
    """
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


# -----------------------------------------------------------------------------
# Logical source
# -----------------------------------------------------------------------------

def logical_source(triples_map):
    """
    Return a SPARQL query that retrieves the source identifier of a single
    logical source (file path, table name, URL, …) for the given triples map.

    Supports rml:logicalSource, the legacy ns0 prefix, and rr:logicalTable.

    Binds:
        ?source   – the source value
        ?label    – rdfs:label of the logical source node (optional)
        ?comment  – rdfs:comment of the logical source node (optional)
    """
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


# -----------------------------------------------------------------------------
# Subject map
# -----------------------------------------------------------------------------

def subject_map_old(triples_map):
    """
    [DEPRECATED] Earlier version of subject_map().

    Fetches the subject map node and its template / reference value.
    Does not capture termType; retained for reference only.
    """
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
    """
    Return a SPARQL query that retrieves the subject map node and its
    template / reference expression for the given triples map.

    Unlike the old variant, this version also captures rr:termType so the
    processor can detect explicit blank-node declarations.

    Binds:
        ?subjectMap  – the subject map blank node or URI
        ?template    – template / reference string (optional)
        ?termType    – explicit term type (e.g. rr:BlankNode) (optional)
        ?label       – rdfs:label (optional)
        ?comment     – rdfs:comment (optional)
    """
    query = f"""
    PREFIX rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX rml: <http://w3id.org/rml/>
    PREFIX ns0: <http://semweb.mmlab.be/ns/rml#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?subjectMap ?template ?termType ?label ?comment
    WHERE {{
        <{triples_map}> (rr:subjectMap|rml:subjectMap) ?subjectMap.

        # Retrieve the template or field reference expression.
        OPTIONAL {{ ?subjectMap (rr:template|rml:template|ns0:reference) ?template. }}

        # Detect explicit blank-node term type if declared.
        OPTIONAL {{ ?subjectMap rr:termType ?termType. }}

        OPTIONAL {{ ?subjectMap rdfs:label ?label. }}
        OPTIONAL {{ ?subjectMap rdfs:comment ?comment. }}
    }}"""
    return query


# -----------------------------------------------------------------------------
# Predicate–object map
# -----------------------------------------------------------------------------

def predicate_object_map_old(triples_map):
    """
    [DEPRECATED] Earlier, simpler version of predicate_object_map().

    Extracts predicate constants and a single merged object value per POM.
    Does not distinguish between constants, references, and templates;
    retained for reference only.
    """
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
    """
    Return a SPARQL query that retrieves predicate–object pairs for the
    given triples map.

    Extracts the predicate from the predicate map and the object value
    (constant, column reference, or template) from the object map.

    Binds:
        ?pr_constant  – the predicate URI
        ?ob_value     – the object value (constant, column name, or template)
    """
    query = f"""
    PREFIX rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX rml: <http://w3id.org/rml/>
    PREFIX ns0: <http://semweb.mmlab.be/ns/rml#>

    SELECT ?pr_constant ?ob_value
    WHERE {{
        <{triples_map}> (rr:predicateObjectMap|rml:predicateObjectMap|ns0:predicateObjectMap) ?pom.

        # Extract the predicate constant or direct predicate shortcut.
        ?pom (rr:predicateMap|rml:predicateMap|ns0:predicateMap) ?pm.
        ?pm (rr:constant|rr:predicate|rml:constant|ns0:constant) ?pr_constant.

        # Extract the object value: constant, column reference, or template.
        ?pom (rr:objectMap|rml:objectMap|ns0:objectMap) ?om.
        ?om (rr:constant|rr:column|rr:template|rml:reference|rml:constant|rml:template|ns0:reference|ns0:constant|ns0:template) ?ob_value.
    }}
    """
    return query


# -----------------------------------------------------------------------------
# Named graph
# -----------------------------------------------------------------------------

def named_graph(triples_map):
    """
    Return a SPARQL query that retrieves any named-graph constant declared
    via rr:subjectMap / rr:graphMap / rr:constant for the given triples map.

    Binds:
        ?graph  – the named graph URI
    """
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


# -----------------------------------------------------------------------------
# Join condition
# -----------------------------------------------------------------------------

def join_condition(triples_map):
    """
    Return a SPARQL query that retrieves all join conditions declared in the
    predicate–object maps of the given triples map.

    A join condition links this (child) triples map to a parent triples map
    via matching key columns.

    Binds:
        ?child             – field name in the child source
        ?parent            – field name in the parent source
        ?parentTriplesMap  – URI of the parent triples map
        ?predicate         – predicate URI that carries the join relationship
        ?s_template        – subject template of the child triples map
        ?o_template        – subject template of the parent triples map
    """
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


# -----------------------------------------------------------------------------
# Logical source (detailed)
# -----------------------------------------------------------------------------

def logical_source_info(triples_map):
    """
    Return a SPARQL query that extracts full logical-source details for the
    given triples map, covering both RML (rml:logicalSource) and R2RML
    (rr:logicalTable) conventions.

    The two source types are handled in separate UNION branches so that
    RML-specific fields (iterator, referenceFormulation) and R2RML-specific
    fields (tableName) are fetched only where applicable.

    Binds:
        ?source                – file path or URL (RML sources)
        ?referenceFormulation  – reference formulation URI (e.g. ql:CSV)
        ?iterator              – JSONPath / XPath iterator expression
        ?sqlQuery              – inline SQL query string (from either vocab)
        ?tableName             – SQL table name (R2RML logicalTable)
    """
    query = f"""
    PREFIX rr: <http://www.w3.org/ns/r2rml#>
    PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

    SELECT DISTINCT ?source ?tableName ?sqlQuery ?iterator ?referenceFormulation
    WHERE {{
        BIND(<{triples_map}> AS ?tm)
        {{
            # Branch 1 — RML logicalSource
            ?tm rml:logicalSource ?ls .
            OPTIONAL {{ ?ls rml:source ?source . }}
            OPTIONAL {{ ?ls rml:referenceFormulation ?referenceFormulation . }}
            OPTIONAL {{ ?ls rml:iterator ?iterator . }}
            OPTIONAL {{ ?ls rr:sqlQuery ?sql1 . }}
            OPTIONAL {{ ?ls rml:query ?sql2 . }}
            # Prefer rr:sqlQuery; fall back to rml:query.
            BIND(COALESCE(?sql1, ?sql2) AS ?sqlQuery)
        }} 
        UNION 
        {{
            # Branch 2 — R2RML logicalTable
            ?tm rr:logicalTable ?lt .
            OPTIONAL {{ ?lt rr:tableName ?tableName . }}
            OPTIONAL {{ ?lt rr:sqlQuery ?sqlQuery . }}
        }}
    }}
    """
    return query


# -----------------------------------------------------------------------------
# Term map info (generic)
# -----------------------------------------------------------------------------

def term_map_info():
    """
    Return a SPARQL query that extracts the value type and content of a
    single term-map node (subject map, predicate map, or object map).

    The query is designed to be executed with an ``initBindings`` dict that
    binds ``?map`` to the specific term-map node being inspected.

    Binds:
        ?constant   – rr:constant value (URI or literal)
        ?template   – rr:template string
        ?reference  – rml:reference field name
        ?column     – rr:column field name (R2RML)
        ?termType   – declared rr:termType (e.g. rr:IRI, rr:BlankNode)
    """
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


# -----------------------------------------------------------------------------
# Predicate–object map info (detailed, used by the processor)
# -----------------------------------------------------------------------------

def pom_info_query_old(triples_map):
    """
    [DEPRECATED] Earlier version of pom_info_query().

    Also fetched ?parentTriplesMap to handle RefObjectMaps, but the FILTER
    and union structure proved redundant. Retained for reference only.
    """
    return f"""
    PREFIX rr: <http://www.w3.org/ns/r2rml#>
    PREFIX rml: <http://semweb.mmlab.be/ns/rml#>

    SELECT DISTINCT ?p ?constant ?template ?reference ?column ?termType ?parentTriplesMap
    WHERE {{
        <{triples_map}> rr:predicateObjectMap ?pom .
        ?pom rr:predicateMap/rr:constant ?p .

        {{
            # Case 1: regular ObjectMap
            ?pom rr:objectMap ?om .
            OPTIONAL {{ ?om rr:constant ?constant . }}
            OPTIONAL {{ ?om rr:template ?template . }}
            OPTIONAL {{ ?om rml:reference ?reference . }}
            OPTIONAL {{ ?om rr:column ?column . }}
            OPTIONAL {{ ?om rr:termType ?termType . }}
        }}
        UNION
        {{
            # Case 2: RefObjectMap (join to another triples map)
            ?pom rr:objectMap ?om .
            ?om rr:parentTriplesMap ?parentTriplesMap .
        }}
    }}
    """


def pom_info_query(triples_map):
    """
    Return a SPARQL query that retrieves all predicate–object map details
    for the given triples map, excluding RefObjectMaps (joins).

    The FILTER at the end ensures that only rows with a concrete object value
    (constant, template, reference, or column) are returned, discarding
    blank object maps that belong to join conditions.

    Binds:
        ?p          – predicate URI
        ?constant   – rr:constant object value (optional)
        ?template   – rr:template object value (optional)
        ?reference  – rml:reference field name (optional)
        ?column     – rr:column field name (optional)
        ?termType   – declared term type for the object (optional)
    """
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
        # Exclude rows where none of the object value types are bound,
        # which would correspond to RefObjectMap (join) entries.
        FILTER (BOUND(?constant) || BOUND(?template) || BOUND(?reference) || BOUND(?column))
    }}
    """