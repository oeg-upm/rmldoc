from rdflib import URIRef
from urllib.parse import urlparse
import os


def prefix_short_cuts(graph, uri):
    if is_valid_uri(str(uri)):
        try:
            shor_curt = URIRef(uri)
            short = shor_curt.n3(graph.namespace_manager)
        except Exception as e:
            print("Warning: URI prefix could not be created:", e)
            short = uri
        # If the resulting string contains '<', it means it's a IRI
        if '<' in short:
            short = shor_curt.toPython()
        # Check if the URI is 'rdf:type' and assign the shorthand 'a'
        if str(short) == 'rdf:type':
            short = 'a'
    else:
        if '{' in uri:
            return uri
        else:
            short = '{' + uri + '}'
    return short


def is_valid_uri(uri):
    if '{' in str(uri):
        return False
    try:
        result = urlparse(uri)
        return all([result.scheme, result.netloc])  # Check if scheme and netloc are present
    except ValueError:
        return False


def is_markdown_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == '.md'


def get_file_name(file_path):
    return os.path.basename(file_path)
