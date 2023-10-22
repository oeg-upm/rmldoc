__author__ = "Jhon Toledo"
__credits__ = ["Jhon Toledo"]
__copyright__ = "Copyright © 2023 Jhon Toledo"

__license__ = "Apache-2.0"
__maintainer__ = "Jhon Toledo"
__email__ = "ja.toledo@upm.es"

import sys
import rdflib
import argparse
import logging
import codecs
import json
import queries
from jinja2 import Environment, FileSystemLoader

log = logging.getLogger("rmd_main")
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
log.handlers.clear()
log.addHandler(ch)


def write_doc(content, output_path):
    """
    :param content:
    :return:
    """
    f = codecs.open(output_path, 'w', "utf-8")
    f.write(content)
    f.close()


def tmp_query(triples_map):
    query = """
    SELECT ?label ?comment ?source ?template
    WHERE {
        <""" + triples_map + """> a rr:TriplesMap.
        <""" + triples_map + """> rml:logicalSource ?logicalSource.
        ?logicalSource rml:source ?source.
        <""" + triples_map + """> rr:subjectMap ?subjectMap.
        ?subjectMap rr:template ?template.
        OPTIONAL {<""" + triples_map + """> rdfs:label ?label }
        OPTIONAL {<""" + triples_map + """> rdfs:comment ?comment. }
    }"""
    return query


def logical_source(triples_map):
    query = """
    SELECT ?source ?label ?comment
    WHERE {
        <""" + triples_map + """> a rr:TriplesMap.
        <""" + triples_map + """> rml:logicalSource ?logicalSource.
        ?logicalSource rml:source ?source.
        OPTIONAL {?logicalSource rdfs:label ?label }
        OPTIONAL {?logicalSource rdfs:comment ?comment. }
    }"""
    return query


def subject_map(triples_map):
    query = """
    SELECT ?template ?label ?comment
    WHERE {
         <""" + triples_map + """> a rr:TriplesMap.
         <""" + triples_map + """> rr:subjectMap ?subjectMap.
        ?subjectMap rr:template ?template.
        OPTIONAL {?subjectMap rdfs:label ?label }
        OPTIONAL {?subjectMap rdfs:comment ?comment. }
    }"""
    return query


def predicate_object_map(triples_map):
    query = """
    SELECT ?pr_constant ?ob_constant
    WHERE {
        <""" + triples_map + """> a rr:TriplesMap.
        <""" + triples_map + """> rr:predicateObjectMap ?predicateObjectMap.
        ?predicateObjectMap rr:predicateMap ?predicateMap.
        ?predicateMap rr:constant  ?pr_constant.
        ?predicateObjectMap rr:objectMap ?objectMap.
        ?objectMap (rr:constant| rml:reference) ?ob_constant
        #OPTIONAL {?predicateObjectMap rdfs:label ?label }
        #OPTIONAL {?predicateObjectMap rdfs:comment ?comment. }
    }
    """
    return query


def workflow(rdf_mapping_path, output_path):
    g = rdflib.Graph()
    g.parse(rdf_mapping_path, format=rdflib.util.guess_format(rdf_mapping_path))  # .ttl format
    environment = Environment(loader=FileSystemLoader("../templates/"))
    template = environment.get_template("rmd.md")
    source_template = environment.get_template("source.md")
    subject_template = environment.get_template("subject.md")
    pom_template = environment.get_template("predicate_object.md")
    spo_diagram = environment.get_template("diagram.md")
    # Prefix
    rmd_prefixes = g.namespaces()
    # Authors
    my_authors = g.query(queries.authors)
    rmd_authors = [{"author": str(author.name), "mbox": str(author.mbox)} for author in my_authors ]
    # mappings
    """TripleMaps"""
    uri_triples_map = g.query(queries.triples_map_query)
    tps_map = {tp.asdict()['TriplesMap'].toPython() for tp in uri_triples_map}
    # print(tps_map)
    mapping_content = ""
    for tp in tps_map:
        # TriplesMap
        mapping_content += f"## {tp}\n"
        # LogicalSource
        source = [{"source": str(i.source), "label": str(i.label), "comment": str(i.comment)} for i in
                  g.query(logical_source(tp))]
        mapping_content += source_template.render(source=source)
        # SubjectMap
        subject = [{"template": str(i.template), "label": str(i.label), "comment": str(i.comment)} for i in
                   g.query(subject_map(tp))]
        mapping_content += subject_template.render(subject=subject)
        # pom = [{"label": str(i.label), "comment": str(i.comment)} for i in g.query(predicate_object_map(tp))]
        # predicateObjectMap
        pom = [{"predicate": str(i.pr_constant), "object": str(i.ob_constant)} for i in
               g.query(predicate_object_map(tp))]
        mapping_content += pom_template.render(pom=pom)
        diagram_subject= subject[0]['template']
        mapping_content += spo_diagram.render(subject=diagram_subject, pom=pom)

    # parse the content
    #content = template.render(authors=rmd_authors, prefixes=rmd_prefixes, mapping_content=mapping_content)
    content = template.render(authors=rmd_authors, prefixes=rmd_prefixes, mapping_content=mapping_content)

    # Write results
    write_doc(content, output_path)


def define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_mapping_path", required=True, help="Input mapping path in RML")
    parser.add_argument("-o", "--output_path", required=True, help="Output path for the generated document")
    return parser


if __name__ == "__main__":
    args = define_args().parse_args()
    log.info("RDF Mapping Documentation(RMD)")
    workflow(args.input_mapping_path, args.output_path)
