__author__ = "Jhon Toledo"
__credits__ = ["Jhon Toledo"]
__copyright__ = "Copyright © 2024 Jhon Toledo"

__license__ = "Apache-2.0"
__maintainer__ = "Jhon Toledo"
__email__ = "ja.toledo@upm.es"

import rdflib
import argparse
import logging
import codecs
from .queries import *
from jinja2 import Environment, FileSystemLoader
from .utils import *

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
    PREFIX rr: <http://www.w3.org/ns/r2rml#>
    SELECT ?label ?comment ?source ?template
    WHERE {
        <""" + triples_map + """>  a rr:TriplesMap.
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
    PREFIX  rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX  rml: <http://w3id.org/rml/>
    PREFIX  ns0: <http://semweb.mmlab.be/ns/rml#>
    SELECT ?source ?label ?comment
    WHERE {
        #<""" + triples_map + """>  a ?TriplesMap.
        <""" + triples_map + """> (ns0:logicalSource|rml:logicalSource) ?logicalSource.
        ?logicalSource (ns0:source|rml:source) ?source.
        OPTIONAL {?logicalSource rdfs:label ?label }
        OPTIONAL {?logicalSource rdfs:comment ?comment. }
    }"""
    return query


def subject_map(triples_map):
    query = """
    PREFIX  rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX  rml: <http://w3id.org/rml/>
    PREFIX  ns0: <http://semweb.mmlab.be/ns/rml#>
    SELECT ?template ?label ?comment
    WHERE {
         #<""" + triples_map + """>  a rr:TriplesMap.
         <""" + triples_map + """> (rr:subjectMap|rml:subjectMap) ?subjectMap.
        ?subjectMap (rr:template|rml:template|ns0:reference) ?template.
        OPTIONAL {?subjectMap rdfs:label ?label }
        OPTIONAL {?subjectMap rdfs:comment ?comment. }
        #FILTER (!isBlank(?template))
    }"""
    return query


def predicate_object_map(triples_map):
    query = """
    PREFIX  rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX  rml: <http://w3id.org/rml/>
    PREFIX  ns0: <http://semweb.mmlab.be/ns/rml#>
    SELECT ?pr_constant ?ob_constant
    WHERE {

        <""" + triples_map + """>  (rr:predicateObjectMap|rml:predicateObjectMap|ns0:predicateObjectMap) ?predicateObjectMap.
        ?predicateObjectMap (rr:predicateMap|rml:predicateMap|ns0:predicateMap)/(rr:constant|rml:constant|ns0:constant) ?pr_constant.
        ?predicateObjectMap (rr:objectMap|rml:objectMap|ns0:objectMap)/((rr:reference|rml:reference|ns0:reference)|(rr:constant|rml:constant|ns0:constant)|(rr:template|rml:template|ns0:template)) ?ob_constant.

        #OPTIONAL {?predicateObjectMap rdfs:label ?label }
        #OPTIONAL {?predicateObjectMap rdfs:comment ?comment. }
    }
    """
    return query


def join_condition(triples_map):
    query = """
    PREFIX  rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX  rml: <http://w3id.org/rml/>
    PREFIX  ns0: <http://semweb.mmlab.be/ns/rml#>
    SELECT distinct *
    WHERE {
        <""" + triples_map + """> rr:predicateObjectMap/rr:objectMap/rr:joinCondition[rr:child ?child; rr:parent ?parent; ^rr:joinCondition/rr:parentTriplesMap ?parentTriplesMap; ^rr:joinCondition/^rr:objectMap/rr:predicateMap/rr:constant ?predicate; ^rr:joinCondition/^rr:objectMap/^rr:predicateObjectMap/rr:subjectMap/rr:template   ?s_template ].
        ?parentTriplesMap rr:subjectMap/(rr:template|ns0:reference) ?o_template.
    }
    """
    return query


def join_condition2(triples_map):
    query = """
    PREFIX  rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX  rml: <http://w3id.org/rml/>
    PREFIX  ns0: <http://semweb.mmlab.be/ns/rml#>
    SELECT distinct ?parentTriplesMap ?parent ?predicate ?child ?o_template ?s_template
    WHERE {
        <""" + triples_map + """> rr:predicateObjectMap/rr:objectMap/rr:joinCondition/rr:child ?child.
        <""" + triples_map + """> rr:predicateObjectMap/rr:objectMap/rr:joinCondition/rr:parent ?parent.
        <""" + triples_map + """> rr:predicateObjectMap/rr:objectMap/rr:parentTriplesMap ?parentTriplesMap.
        ?parentTriplesMap rr:subjectMap/rr:template ?o_template.
        ?parentTriplesMap ^(rr:parentTriplesMap)/^(rr:objectMap) ?p.
        ?p rr:predicateMap/rr:constant ?predicate.
        ?parentTriplesMap ^(rr:parentTriplesMap)/^(rr:objectMap)/^(rr:predicateObjectMap) ?subject.
        ?subject rr:subjectMap/rr:template ?s_template.
    }
    """
    return query


def get_namespaces(g):
    g1 = rdflib.Graph()
    temp1 = g.namespaces()
    temp2 = g1.namespaces()
    return list(set(temp1) - set(temp2))


def workflow(rdf_mapping_path, output_path):
    g = rdflib.Graph()
    g.parse(rdf_mapping_path, format=rdflib.util.guess_format(rdf_mapping_path))  # .ttl format
    environment = Environment(loader=FileSystemLoader("../Templates/"))
    template = environment.get_template("rmd.md")
    source_template = environment.get_template("source.md")
    subject_template = environment.get_template("subject.md")
    pom_template = environment.get_template("predicate_object.md")
    spo_diagram = environment.get_template("diagram.md")
    join_diagram = environment.get_template("function.md")
    # Prefix
    # rmd_prefixes = g.namespaces()
    rmd_prefixes = get_namespaces(g)
    # Authors
    my_authors = g.query(authors)
    rmd_authors = [{"author": str(author.name), "mbox": str(author.mbox)} for author in my_authors]

    # mappings
    """TripleMaps"""
    uri_triples_map = g.query(triples_map_query)
    tps_map = {tp.asdict()['triplesMap'].toPython() for tp in uri_triples_map}
    mapping_content = ""

    for tp in tps_map:
        # TriplesMap label
        mapping_content += f"## {tp.split('/')[-1]}\n"

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
        pom = [{"predicate": str(i.pr_constant), "object": str(prefix_short_cuts(g, i.ob_constant))} for i in
               g.query(predicate_object_map(tp))]

        pom_diagram = [{"predicate": str(prefix_short_cuts(g, i.pr_constant)),
                        "object": str(prefix_short_cuts(g, i.ob_constant))} for i in
                       g.query(predicate_object_map(tp))]

        mapping_content += pom_template.render(pom=pom)
        if subject:
            # PO diagram
            diagram_subject = subject[0]['template']
            mapping_content += spo_diagram.render(subject=diagram_subject, pom=pom_diagram)

        # join diagram
        join_condition_diagram = [
            {"predicate": str(prefix_short_cuts(g, i.predicate)),
             "parentTriplesMap": str(i.parentTriplesMap).split('/')[-1],
             "child": str(i.child), "parent": str(i.parent), 'template': str(i.o_template),
             'subject': str(i.s_template)} for i in
            g.query(join_condition(tp))]

        # print(join_condition_diagram)
        mapping_content += join_diagram.render(subject=tp.split('/')[-1], join_list=join_condition_diagram)

    # parse the content
    # content = template.render(authors=rmd_authors, prefixes=rmd_prefixes, mapping_content=mapping_content)
    content = template.render(mapping_file=get_file_name(rdf_mapping_path), authors=rmd_authors, prefixes=rmd_prefixes,
                              mapping_content=mapping_content)

    # Write results
    write_doc(content, output_path)


def define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_mapping_path", required=True,
                        help="Path to the input mapping file in RML format.")
    parser.add_argument("-o", "--output_path", default="output.md", required=False,
                        help="Path to save the generated document. Default output output.md")
    return parser


if __name__ == "__main__":
    args = define_args().parse_args()
    log.info("RML Mapping Documentation(RMLdoc)")
    workflow(args.input_mapping_path, args.output_path)
