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
from jinja2 import Environment, FileSystemLoader, PackageLoader
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
    if not is_markdown_file(output_path):
        output_path = output_path + ".md"
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
        <""" + triples_map + """> (ns0:logicalSource|rml:logicalSource|rr:logicalTable) ?logicalSource.
        ?logicalSource (ns0:source|rml:source|rr:tableName) ?source.
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
        ?predicateObjectMap (rr:predicateMap|rml:predicateMap|ns0:predicateMap)/(rr:constant|rml:constant|ns0:constant)|(rr:predicate) ?pr_constant.
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


def named_graph(triples_map):
    query = """
    PREFIX  rr: <http://www.w3.org/ns/r2rml#> 
    PREFIX  rml: <http://w3id.org/rml/>
    PREFIX  ns0: <http://semweb.mmlab.be/ns/rml#>
    SELECT distinct ?graph
    WHERE {
        <""" + triples_map + """> rr:subjectMap/rr:graphMap/rr:constant ?graph .
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
    # environment = Environment(loader=FileSystemLoader("../templates/"))
    path = os.path.join(os.path.dirname(__file__), 'Templates/')
    templateLoader = FileSystemLoader(searchpath=path)
    environment = Environment(loader=templateLoader)

    template = environment.get_template("rmd.md")
    source_template = environment.get_template("source.md")
    subject_template = environment.get_template("subject.md")
    pom_template = environment.get_template("predicate_object.md")
    spo_diagram = environment.get_template("diagram.md")
    join_diagram = environment.get_template("function.md")
    named_graph_template = environment.get_template("named_graph.md")
    # Version
    rml_version = g.query(dataset_version)

    rml_version = [{"version": str(vr.version), "license": str(vr.license), "description": str(vr.description),
                    "title": str(vr.title), "dateCreated": str(vr.dateCreated)} for vr in rml_version]

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

        pom_diagram = [{"predicate": str(prefix_short_cuts(g, (str(i.pr_constant)).replace('"', "'"))),
                        "object": str(prefix_short_cuts(g, (str(i.ob_constant)).replace('"', "'")))} for i in
                       g.query(predicate_object_map(tp))]
        if subject:
            # PO diagram
            diagram_subject = str(subject[0]['template']).replace('"', "'")

        if pom_diagram:
            mapping_content += pom_template.render(pom=pom_diagram)
            mapping_content += spo_diagram.render(subject=diagram_subject, pom=pom_diagram)

            # mapping_content += spo_diagram.render(subject=diagram_subject, pom=pom_diagram)

        # join diagram
        join_condition_diagram = [
            {"predicate": str(prefix_short_cuts(g, i.predicate)),
             "parentTriplesMap": str(i.parentTriplesMap).split('/')[-1],
             "child": str(i.child), "parent": str(i.parent), 'template': str(i.o_template).replace('"', "'"),
             'subject': str(i.s_template).replace('"', "'")} for i in
            g.query(join_condition(tp))]

        if join_condition_diagram:
            mapping_content += join_diagram.render(subject=tp.split('/')[-1], join_list=join_condition_diagram)

        # named_graph
        rml_graph = [{"graph": str(i.graph)} for i in g.query(named_graph(tp))]
        if rml_graph:
            mapping_content += named_graph_template.render(graph=rml_graph)

    # parse the content
    # content = template.render(authors=rmd_authors, prefixes=rmd_prefixes, mapping_content=mapping_content)

    content = template.render(version=rml_version, mapping_file=get_file_name(rdf_mapping_path),
                              authors=rmd_authors,
                              prefixes=rmd_prefixes,
                              mapping_content=mapping_content)
    # Write results
    write_doc(content, output_path)


def workflow_with_yatter(rdf_mapping_path, output_path):
    import yatter
    from ruamel.yaml import YAML
    yaml = YAML(typ='safe', pure=True)
    rml_content = yatter.translate(yaml.load(open(rdf_mapping_path)))

    g = rdflib.Graph()
    g.parse(data=rml_content)  # .ttl format
    # environment = Environment(loader=FileSystemLoader("../templates/"))
    path = os.path.join(os.path.dirname(__file__), 'Templates/')
    templateLoader = FileSystemLoader(searchpath=path)
    environment = Environment(loader=templateLoader)

    template = environment.get_template("rmd.md")
    source_template = environment.get_template("source.md")
    subject_template = environment.get_template("subject.md")
    pom_template = environment.get_template("predicate_object.md")
    spo_diagram = environment.get_template("diagram.md")
    join_diagram = environment.get_template("function.md")
    named_graph_template = environment.get_template("named_graph.md")
    # Version
    rml_version = g.query(dataset_version)

    rml_version = [{"version": str(vr.version), "license": str(vr.license), "description": str(vr.description),
                    "title": str(vr.title), "dateCreated": str(vr.dateCreated)} for vr in rml_version]

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

        pom_diagram = [{"predicate": str(prefix_short_cuts(g, (str(i.pr_constant)).replace('"', "'"))),
                        "object": str(prefix_short_cuts(g, (str(i.ob_constant)).replace('"', "'")))} for i in
                       g.query(predicate_object_map(tp))]
        if subject:
            # PO diagram
            diagram_subject = str(subject[0]['template']).replace('"', "'")

        if pom_diagram:
            mapping_content += pom_template.render(pom=pom_diagram)
            mapping_content += spo_diagram.render(subject=diagram_subject, pom=pom_diagram)

            # mapping_content += spo_diagram.render(subject=diagram_subject, pom=pom_diagram)

        # join diagram
        join_condition_diagram = [
            {"predicate": str(prefix_short_cuts(g, i.predicate)),
             "parentTriplesMap": str(i.parentTriplesMap).split('/')[-1],
             "child": str(i.child), "parent": str(i.parent), 'template': str(i.o_template).replace('"', "'"),
             'subject': str(i.s_template).replace('"', "'")} for i in
            g.query(join_condition(tp))]

        if join_condition_diagram:
            mapping_content += join_diagram.render(subject=tp.split('/')[-1], join_list=join_condition_diagram)

        # named_graph
        rml_graph = [{"graph": str(i.graph)} for i in g.query(named_graph(tp))]
        if rml_graph:
            mapping_content += named_graph_template.render(graph=rml_graph)

    content = template.render(version=rml_version, mapping_file=get_file_name(rdf_mapping_path),
                              authors=rmd_authors,
                              prefixes=rmd_prefixes,
                              mapping_content=mapping_content)
    # Write results
    write_doc(content, output_path)


def define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_mapping_path", required=True,
                        help="Path to the input mapping file in RML format.")
    parser.add_argument("-o", "--output_path", default="output.md", required=False,
                        help="Path to save the generated document. Default output output.md")
    parser.add_argument("-y", "--yatter", action='store_true',
                        help="Enable yatter option to read yarrrml mappings")
    return parser


def main():

    args = define_args().parse_args()
    log.info("RML Documentation(RMLdoc)")
    log.info(args.input_mapping_path)
    if args.yatter:
        workflow_with_yatter(args.input_mapping_path, args.output_path)
    else:
        workflow(args.input_mapping_path, args.output_path)


if __name__ == "__main__":
    main()
