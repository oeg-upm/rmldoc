"""
RMLDoc CLI - Generate documentation from RML/YARRRML mappings.
"""

__author__ = "Jhon Toledo"
__credits__ = ["Jhon Toledo"]
__copyright__ = "Copyright © 2024 Jhon Toledo"
__license__ = "Apache-2.0"
__maintainer__ = "Jhon Toledo"
__email__ = "ja.toledo@upm.es"

import argparse
import logging
import sys
import subprocess
from pathlib import Path

# rdflib imports used for metadata injection into the RDF graph.
import rdflib
from rdflib import Graph, Literal, URIRef, BNode, Namespace
from rdflib.namespace import RDF, RDFS

from rmldoc.workflows import workflow_md, workflow_html


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    """Configure and return the application logger."""
    logger = logging.getLogger("rmd_main")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger

log = setup_logging()


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """
    Define and parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate documentation from RML/YARRRML mappings.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-i", "--input_mapping_path",
        required=True,
        type=Path,
        help="Path to the input mapping file (.ttl, .yml, etc.)."
    )
    parser.add_argument(
        "-o", "--output_path",
        default=Path("output.md"),
        type=Path,
        help="Path to save the generated document."
    )
    parser.add_argument(
        "-y", "--yatter",
        action='store_true',
        help="Enable explicit YARRRML support. (Auto-detected for .yml inputs; use this to force .yml generation from .ttl)."
    )
    parser.add_argument(
        "-f", "--format",
        choices=["md", "html"],
        default="md",
        help="Specify output format: 'md' for Markdown or 'html' for HTML."
    )

    meta_group = parser.add_argument_group(
        'Optional Metadata',
        'Inject metadata directly into the generated/existing RML mapping (.ttl file)'
    )
    meta_group.add_argument("--title",   type=str, help="Title of the dataset/mapping")
    meta_group.add_argument("--desc",    type=str, help="Description of the mapping")
    meta_group.add_argument("--version", type=str, help="Version (e.g., 1.0.0)")
    meta_group.add_argument("--date",    type=str, help="Creation date (e.g., 14-02-2026)")

    for i in range(1, 11):
        meta_group.add_argument(f"--author{i}", type=str, help=f"Author {i} name")
        meta_group.add_argument(f"--email{i}",  type=str, help=f"Author {i} email")

    return parser.parse_args()


# ---------------------------------------------------------------------------
# Yatter integration
# ---------------------------------------------------------------------------

def run_yatter(input_file: Path, output_file: Path) -> None:
    """
    Invoke the yatter CLI module as a subprocess to convert between
    YARRRML (.yml) and RML (.ttl) serialisations.
    """
    try:
        import yatter
    except ImportError:
        log.error("The 'yatter' package is not installed. Please install it using: pip install yatter")
        sys.exit(1)

    cmd = [sys.executable, "-m", "yatter", "-i", str(input_file), "-o", str(output_file)]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        log.error(f"Error executing yatter:\n{e.stderr}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# Metadata injection
# ---------------------------------------------------------------------------

def inject_metadata(ttl_path: Path, args: argparse.Namespace) -> None:
    """
    Inject dataset metadata supplied via CLI arguments into the Turtle file.
    """
    has_metadata = any([args.title, args.desc, args.version, args.date]) or \
                   any(getattr(args, f"author{i}", None) or getattr(args, f"email{i}", None) for i in range(1, 11))

    if not has_metadata:
        return

    log.info(f"Injecting metadata into {ttl_path.name}...")

    g = Graph()
    try:
        g.parse(ttl_path, format="turtle")
    except Exception as e:
        log.error(f"Failed to parse {ttl_path} for metadata injection: {e}")
        return

    SCHEMA = Namespace("http://schema.org/")
    DCT    = Namespace("http://purl.org/dc/terms/")
    FOAF   = Namespace("http://xmlns.com/foaf/0.1/")

    g.bind("schema", SCHEMA)
    g.bind("dct",    DCT)
    g.bind("foaf",   FOAF)

    dataset_node = next(g.subjects(RDF.type, SCHEMA.Dataset), None)
    if not dataset_node:
        dataset_node = BNode()
        g.add((dataset_node, RDF.type, SCHEMA.Dataset))

    if args.title:
        g.set((dataset_node, SCHEMA.title,       Literal(args.title)))
    if args.desc:
        g.set((dataset_node, SCHEMA.description, Literal(args.desc)))
    if args.version:
        g.set((dataset_node, SCHEMA.version,     Literal(args.version)))
    if args.date:
        g.set((dataset_node, SCHEMA.dateCreated, Literal(args.date)))

    for i in range(1, 11):
        author = getattr(args, f"author{i}", None)
        email  = getattr(args, f"email{i}",  None)

        if author or email:
            person_node = BNode()
            g.add((person_node, RDF.type, FOAF.Person))

            if author:
                g.add((person_node, RDFS.label, Literal(author)))
            if email:
                email_uri = email if email.startswith("mailto:") else f"mailto:{email}"
                g.add((person_node, FOAF.mbox, URIRef(email_uri)))

            g.add((dataset_node, SCHEMA.contributor, person_node))

    g.serialize(destination=str(ttl_path), format="turtle")
    log.info("Metadata successfully injected.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    log.info("Starting RML Documentation generation.")
    log.info(f"Input Mapping Path: {args.input_mapping_path}")
    log.info(f"Output Format: {args.format}")

    input_path:  Path = args.input_mapping_path
    output_path: Path = args.output_path

    # ------------------------------------------------------------------
    # File Format Detection & Yatter Integration
    # ------------------------------------------------------------------
    is_yaml = input_path.suffix.lower() in [".yml", ".yaml"]
    is_ttl  = input_path.suffix.lower() in [".ttl", ".rml", ".nt"]

    if is_yaml:
        # Si es un YAML, ignoramos si se pasó la bandera -y o no, siempre usamos yatter.
        output_ttl_path = input_path.with_suffix(".ttl")
        log.info(f"YARRRML input detected (.yml). Automatically using yatter to generate RML serialization ({output_ttl_path.name})...")
        run_yatter(input_path, output_ttl_path)

        # Actualizamos la ruta al archivo .ttl recién generado
        input_path = output_ttl_path

    elif is_ttl:
        # Si es TTL, solo invocamos yatter si el usuario quiere generar el YAML de respaldo explícitamente.
        if args.yatter:
            output_yml_path = input_path.with_suffix(".yml")
            if not output_yml_path.exists():
                log.info(f"RML input detected (.ttl) and --yatter flag used. Generating missing YARRRML serialization ({output_yml_path.name})...")
                run_yatter(input_path, output_yml_path)

    # ------------------------------------------------------------------
    # Metadata injection
    # ------------------------------------------------------------------
    # En este punto garantizamos que input_path es un .ttl
    inject_metadata(input_path, args)

    # Corregimos la extensión si no cuadra con el formato pedido
    expected_ext = f".{args.format}"
    if output_path.suffix != expected_ext:
        output_path = output_path.with_suffix(expected_ext)

    # ------------------------------------------------------------------
    # Workflow execution
    # ------------------------------------------------------------------
    try:
        if args.format == "html":
            workflow_html(input_path, str(output_path))
        else:
            workflow_md(str(input_path), str(output_path))

        log.info(f"Documentation successfully generated at: {output_path}")

    except Exception as e:
        log.error("An error occurred during the workflow execution.", exc_info=e)
        sys.exit(1)


if __name__ == "__main__":
    main()