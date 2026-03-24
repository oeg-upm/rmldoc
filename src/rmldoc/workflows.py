__author__ = "Jhon Toledo"
__credits__ = ["Jhon Toledo"]
__copyright__ = "Copyright © 2024 Jhon Toledo"
__license__ = "Apache-2.0"
__maintainer__ = "Jhon Toledo"
__email__ = "ja.toledo@upm.es"

import json
import logging
import os
import codecs
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

from rmldoc.processor import RMLDocProcessor

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

log = logging.getLogger("workflow")
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
log.handlers.clear()
log.addHandler(ch)

# CDN fallback URL for Cytoscape.js (used only if the local bundle is absent).
CYTOSCAPE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.26.0/cytoscape.min.js"


# -----------------------------------------------------------------------------
# Template loaders
# -----------------------------------------------------------------------------

def load_markdown_templates():
    """
    Load all Jinja2 templates required for Markdown output.

    Templates are read from the ``Templates/md/`` directory relative to this
    module's location.

    Returns a dict mapping logical names to compiled ``Template`` objects:

    ``main``         – top-level document wrapper (rmd.md)
    ``source``       – logical-source section (source.md)
    ``subject``      – subject-map section (subject.md)
    ``pom``          – predicate–object table (predicate_object.md)
    ``spo_diagram``  – Mermaid SPO diagram (diagram.md)
    ``join_diagram`` – Mermaid join diagram (function.md)
    ``named_graph``  – named-graph section (named_graph.md)
    """
    path = os.path.join(os.path.dirname(__file__), 'Templates', 'md')
    template_loader = FileSystemLoader(searchpath=path)
    environment = Environment(loader=template_loader)

    return {
        "main": environment.get_template("rmd.md"),
        "source": environment.get_template("source.md"),
        "subject": environment.get_template("subject.md"),
        "pom": environment.get_template("predicate_object.md"),
        "spo_diagram": environment.get_template("diagram.md"),
        "join_diagram": environment.get_template("function.md"),
        "named_graph": environment.get_template("named_graph.md"),
    }


def load_html_templates():
    """
    Load all Jinja2 templates, CSS, and JavaScript required for HTML output.

    Templates are read from ``Templates/html/templates/``, CSS from
    ``Templates/html/css/styles.css``, and JS from
    ``Templates/html/js/scripts.js`` (optional — empty string if absent).

    Returns a dict with:

    ``main``  – compiled index.html template
    ``css``   – raw CSS text to be inlined in the rendered page
    ``js``    – raw JS text to be inlined in the rendered page (may be empty)
    """
    base = os.path.dirname(__file__)
    html_dir = os.path.join(base, "Templates", "html")

    # Load Jinja2 templates from the html/templates/ subdirectory.
    template_loader = FileSystemLoader(searchpath=os.path.join(html_dir, "templates"))
    environment = Environment(loader=template_loader)

    # Read CSS to be embedded inline in the output HTML.
    css_path = os.path.join(html_dir, "css", "styles.css")
    with open(css_path, "r", encoding="utf-8") as f:
        css_text = f.read()

    # Read JS to be embedded inline; gracefully skip if the file does not exist.
    js_path = os.path.join(html_dir, "js", "scripts.js")
    js_text = ""
    if os.path.isfile(js_path):
        with open(js_path, "r", encoding="utf-8") as f:
            js_text = f.read()

    return {
        "main": environment.get_template("index.html"),
        "css": css_text,
        "js": js_text,
    }


def write_documentation(content, output_path):
    """Write the rendered documentation string to *output_path* using UTF-8 encoding."""
    with codecs.open(output_path, 'w', "utf-8") as f:
        f.write(content)


# -----------------------------------------------------------------------------
# Markdown workflow
# -----------------------------------------------------------------------------

def workflow_md(rdf_mapping_path, output_path):
    """
    Full pipeline for generating Markdown documentation from an RML mapping.

    Steps:
    1. Parse the mapping file with :class:`RMLDocProcessor`.
    2. Extract dataset metadata, custom prefixes, and all triples-map data.
    3. Adapt the data to the format expected by the Markdown templates.
    4. Render each triples-map section and assemble the final document.
    5. Write the result to *output_path*.
    """
    templates = load_markdown_templates()

    # Parse the mapping file and extract all structured data.
    rml_doc = RMLDocProcessor(Path(rdf_mapping_path))
    meta = rml_doc.extract_mapping_metadata()
    rmd_prefixes = rml_doc.prefix_map
    maps = rml_doc.build_triples_maps()

    # Reshape metadata into the list format expected by the main template.
    rml_version = [{
        "version": meta.get("version", ""),
        "license": meta.get("license_url", ""),
        "description": meta.get("description", ""),
        "title": meta.get("title", ""),
        "dateCreated": meta.get("date_created", ""),
    }]

    rmd_authors = [{"author": a["name"], "mbox": a["mbox"]} for a in meta.get("authors", [])]
    prefixes_list = list(rmd_prefixes.items())

    # Build the per-triples-map body content.
    mapping_content = generate_mapping_content_md(maps, templates)

    # Render the top-level document template and write to disk.
    content = templates["main"].render(
        version=rml_version,
        mapping_file=meta.get("mapping_filename", ""),
        authors=rmd_authors,
        prefixes=prefixes_list,
        mapping_content=mapping_content,
    )

    write_documentation(content, output_path)


def generate_mapping_content_md(maps, templates):
    """
    Render a Markdown section for each triples map and concatenate the results.

    Each section contains, in order:
    1. A level-2 heading with the triples-map ID.
    2. The logical-source block (if a source value is present).
    3. The subject-map block.
    4. The predicate–object table and its Mermaid SPO diagram (if predicates exist).
    5. The join-condition Mermaid diagram (if join conditions exist).
    6. The named-graph block (if a named graph is declared).

    Returns the full Markdown body as a single string.
    """
    mapping_sections = []

    for m in maps:
        section_parts = [f"## {m['id']}\n"]

        # --- 1. Logical source ---
        # Use the first available source descriptor: file/URL, table name,
        # inline SQL query, or iterator expression.
        src_val = (
                m["source_info"].get("source")
                or m["source_info"].get("tableName")
                or m["source_info"].get("sqlQuery")
                or m["source_info"].get("iterator")
        )
        if src_val:
            section_parts.append(templates["source"].render(source=[{"source": src_val}]))

        # --- 2. Subject map ---
        subject_val = m.get("subject_raw") or m.get("subject")
        if subject_val:
            section_parts.append(templates["subject"].render(subject=[{"template": subject_val}]))

        # --- 3. Predicate–object map table and SPO diagram ---
        if m.get("predicates"):
            pom_list = [{"predicate": p["p"], "object": p["o_display"]} for p in m["predicates"]]

            try:
                section_parts.append(templates["pom"].render(pom=pom_list))
            except Exception as e:
                log.warning(f"Error rendering POM for {m['id']}: {e}")

            # Render the Mermaid diagram alongside the predicate table.
            section_parts.append(templates["spo_diagram"].render(
                subject=subject_val,
                pom=pom_list,
            ))

        # --- 4. Join conditions diagram ---
        if m.get("joins") and len(m["joins"]) > 0:
            join_list = []
            for j in m["joins"]:
                join_list.append({
                    "parentTriplesMap": j["parent_tm"],
                    "child": j["child"],
                    "parent": j["parent"],
                    "predicate": j.get("predicate", "join"),
                    "subject": j.get("s_template", m["id"]),
                    "template": j.get("o_template", j["parent_tm"]),
                })
            section_parts.append(templates["join_diagram"].render(
                subject=m["id"],
                join_list=join_list,
            ))

        # --- 5. Named graph ---
        if m.get("graph"):
            section_parts.append(templates["named_graph"].render(graph=[{"graph": m["graph"]}]))

        mapping_sections.append("".join(section_parts))

    return "".join(mapping_sections)


# -----------------------------------------------------------------------------
# HTML workflow
# -----------------------------------------------------------------------------

def workflow_html(rdf_mapping_path, output_path):
    """
    Full pipeline for generating self-contained HTML documentation from an
    RML mapping.

    Steps:
    1. Load the local Cytoscape.js bundle to embed it inline (no CDN required).
    2. Parse the mapping file with :class:`RMLDocProcessor`.
    3. Extract dataset metadata, custom prefixes, and all triples-map data.
    4. Build a JSON payload consumed by the Cytoscape graph renderer in the browser.
    5. Render the index.html template with all data and assets inlined.
    6. Write the result to *output_path*.
    """
    PACKAGE_ROOT = Path(__file__).parent
    cytoscape_path = (
            PACKAGE_ROOT / "Templates" / "html" / "ajax" / "libs"
            / "cytoscape" / "3.26.0" / "cytoscape.min.js"
    )

    # Read the bundled Cytoscape library to inline it in the output HTML,
    # making the file fully self-contained without network dependencies.
    with open(cytoscape_path, "r", encoding="utf-8") as f:
        cytoscape_js_content = f.read()

    templates = load_html_templates()
    rml_doc = RMLDocProcessor(Path(rdf_mapping_path))

    meta = rml_doc.extract_mapping_metadata()
    rmd_prefixes = rml_doc.prefix_map
    maps = rml_doc.build_triples_maps()

    # Build the data payload passed to the browser-side Cytoscape renderer.
    # ``maps``       – keyed by triples-map ID for fast lookup.
    # ``containers`` – maps each ID to its DOM element ID for graph mounting.
    payload = {
        "maps": {m["id"]: m for m in maps},
        "containers": {m["id"]: f"cy_{rml_doc.safe_id(m['id'])}" for m in maps},
    }

    # Render the single-file HTML document with all assets inlined.
    content = templates["main"].render(
        **meta,
        prefixes=dict(rmd_prefixes),
        maps_list=maps,
        payload_json=json.dumps(payload, ensure_ascii=False),
        containers=payload["containers"],
        css=templates["css"],
        js=templates["js"],
        cytoscape_lib=cytoscape_js_content,
    )

    write_documentation(content, output_path)
