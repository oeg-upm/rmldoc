from pathlib import Path
from typing import Any, Optional

from rdflib import Graph, Literal, Namespace, RDF
from rdflib.namespace import RDFS
import re

from rmldoc.queries import (
    logical_source_info,
    pom_info_query,
    subject_map,
    term_map_info,
    triples_map_query,
    join_condition,
    named_graph,
)

# ---------------------------------------------------------------------------
# Namespace declarations
#
# These namespaces are used throughout the module to construct and identify
# RDF terms in the mapping graph. Each constant maps a short prefix to its
# full URI base.
# ---------------------------------------------------------------------------
RR     = Namespace("http://www.w3.org/ns/r2rml#")          # R2RML vocabulary
RML    = Namespace("http://semweb.mmlab.be/ns/rml#")         # RML extension
RDFNS  = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")  # RDF core
SCHEMA = Namespace("http://schema.org/")                    # Schema.org metadata
DCT    = Namespace("http://purl.org/dc/terms/")             # Dublin Core Terms
FOAF   = Namespace("http://xmlns.com/foaf/0.1/")            # FOAF (people/agents)
QL     = Namespace("http://semweb.mmlab.be/ns/ql#")         # Query Language vocab

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

# Full URI of rdf:type, used to normalise predicate display to the "a" shorthand.
_RDF_TYPE_URI = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"


# ---------------------------------------------------------------------------
# Main processor class
# ---------------------------------------------------------------------------

class RMLDocProcessor:
    """
    Parses an RML mapping file (Turtle syntax) and exposes structured data
    about its triples maps, logical sources, subject maps, predicates,
    join conditions, named graphs, and dataset-level metadata.

    This class is the central entry point for rmldoc's document generation
    pipeline: instantiate it with a path to a .ttl mapping file, then call
    the various ``build_*`` / ``extract_*`` / ``parse_*`` methods to
    retrieve the information needed to render documentation.
    """

    # ------------------------------------------------------------------
    # Construction & graph loading
    # ------------------------------------------------------------------

    def __init__(self, mapping_path: Path):
        """
        Load and parse the RML mapping file at *mapping_path*.

        After construction the following attributes are available:

        * ``self.graph``      – the parsed ``rdflib.Graph``
        * ``self.prefix_map`` – custom prefixes declared in the mapping
        """
        self.mapping_path = mapping_path
        self.graph = self._load_graph(mapping_path)
        self.prefix_map = self._get_custom_prefixes()

    def _load_graph(self, mapping_path: Path) -> Graph:
        """
        Parse the Turtle file into an rdflib Graph and register all
        namespace prefixes declared in the file so that ``get_qname``
        can compress URIs back to CURIEs (e.g. ``esdir:DireccionPostal``).
        """
        graph = Graph()
        graph.parse(location=str(mapping_path), format="turtle")

        # Re-bind every prefix so the namespace manager can normalise URIs
        # to their CURIE form later.
        for prefix, uri in graph.namespaces():
            graph.namespace_manager.bind(prefix, uri, override=True)

        return graph

    # ------------------------------------------------------------------
    # Identifier & prefix helpers
    # ------------------------------------------------------------------

    @staticmethod
    def safe_id(s: str) -> str:
        """
        Convert an arbitrary string into a safe CSS/HTML identifier by
        replacing every non-alphanumeric character with an underscore.
        """
        return re.sub(r"[^A-Za-z0-9_]", "_", s)

    @staticmethod
    def get_id_from_tm(tm: str) -> str:
        """
        Extract a short human-readable identifier from a triples-map URI.

        Takes the last path segment after stripping a trailing slash, e.g.
        ``http://example.org/mapping/Person`` → ``"Person"``.
        """
        return tm.rstrip("/").rsplit("/", 1)[-1]

    def _get_custom_prefixes(self) -> dict:
        """
        Return only the *application-specific* prefixes declared in the
        mapping file, filtering out the standard rdflib default prefixes
        (rdf, rdfs, owl, xsd, …).
        """
        default_prefixes = dict(Graph().namespaces()).keys()
        return {
            prefix: str(uri)
            for prefix, uri in self.graph.namespaces()
            if prefix and prefix not in default_prefixes
        }

    # ------------------------------------------------------------------
    # Graph access helpers
    # ------------------------------------------------------------------

    def get_first_obj(self, subject: Any, predicate: Any) -> Optional[Any]:
        """
        Return the first object found for (*subject*, *predicate*) in the
        graph, or ``None`` if no triple matches.
        """
        return next(self.graph.objects(subject, predicate), None)

    def get_qname(self, term: Any) -> str:
        """
        Compress an rdflib term to its CURIE / prefixed-name representation.

        * ``Literal`` values are returned as plain strings.
        * URIRefs are normalised through the graph's namespace manager
          (e.g. ``http://schema.org/name`` → ``schema:name``).
        * If normalisation fails, the raw string form is returned.
        """
        if term is None:
            return ""
        if isinstance(term, Literal):
            return str(term)
        try:
            return self.graph.namespace_manager.normalizeUri(term)
        except Exception:
            return str(term)

    def expand_curie(self, value: str) -> Optional[str]:
        """
        Expand a CURIE string (e.g. ``schema:name``) to its full URI.

        Returns ``None`` if the prefix is unknown or expansion fails.
        """
        try:
            return str(self.graph.namespace_manager.expand_curie(value))
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Dataset-level metadata
    # ------------------------------------------------------------------

    def extract_mapping_metadata(self) -> dict:
        """
        Extract documentation metadata from the ``schema:Dataset`` node
        declared in the mapping file.

        Returns a dictionary with the following keys:

        ``title``
            Human-readable title of the mapping, falling back to the
            filename if absent.
        ``version``
            Version string (``"0.0.0"`` if not specified).
        ``date_created``
            ISO date string or empty string.
        ``description``
            Free-text description or empty string.
        ``license_url``
            License URI from ``schema:license`` or ``dct:license``.
        ``authors``
            List of ``{"name": …, "mbox": …}`` dicts from
            ``schema:contributor`` nodes.
        ``mapping_filename``
            Basename of the Turtle file.
        ``yarrrml_file``
            Corresponding YARRRML filename (same stem, ``.yml`` extension).
        """
        # Prefer a Dataset node that also carries a title; fall back to the
        # first Dataset node found.
        ds_node = next(
            (
                s for s in self.graph.subjects(RDF.type, SCHEMA.Dataset)
                if self.get_first_obj(s, SCHEMA.title)
            ),
            next(self.graph.subjects(RDF.type, SCHEMA.Dataset), None),
        )

        meta = {
            "title": str(
                self.get_first_obj(ds_node, SCHEMA.title)
                or f"Mapping Documentation ({self.mapping_path.name})"
            ),
            "version":      str(self.get_first_obj(ds_node, SCHEMA.version)     or "0.0.0"),
            "date_created": str(self.get_first_obj(ds_node, SCHEMA.dateCreated) or ""),
            "description":  str(self.get_first_obj(ds_node, SCHEMA.description) or ""),
            "license_url":  str(
                self.get_first_obj(ds_node, SCHEMA.license)
                or self.get_first_obj(ds_node, DCT.license)
                or ""
            ),
            "authors":           [],
            "mapping_filename":  self.mapping_path.name,
            "yarrrml_file":      self.mapping_path.with_suffix(".yml").name,
        }

        # Collect contributor information (name + email) when available.
        if ds_node:
            for person in self.graph.objects(ds_node, SCHEMA.contributor):
                name = str(self.get_first_obj(person, RDFS.label) or "")
                mbox = self.get_first_obj(person, FOAF.mbox)
                if name:
                    meta["authors"].append({
                        "name": name,
                        "mbox": str(mbox) if mbox else "",
                    })

        return meta

    # ------------------------------------------------------------------
    # Logical source parsing
    # ------------------------------------------------------------------

    def parse_logical_source(self, tm_uri) -> dict:
        """
        Extract logical-source details for the triples map at *tm_uri*.

        The returned dictionary has the following keys:

        ``kind``
            Detected source type: ``"CSV"``, ``"JSON"``, ``"XML"``,
            ``"SQL"``, or ``"Other"``.
        ``source``
            Raw source value (file path, URL, …).
        ``referenceFormulation``
            CURIE of the reference formulation (e.g. ``ql:CSV``).
        ``iterator``
            JSONPath / XPath iterator expression (empty for CSV/SQL).
        ``sqlQuery``
            Inline SQL query string, if any.
        ``tableName``
            SQL table name, if any.
        """
        info = {
            "kind":                 "Other",
            "source":               "",
            "referenceFormulation": "",
            "iterator":             "",
            "sqlQuery":             "",
            "tableName":            "",
        }

        for row in self.graph.query(logical_source_info(tm_uri)):
            info["source"]    = str(row.source    or "")
            info["tableName"] = str(row.tableName or "")
            info["sqlQuery"]  = str(row.sqlQuery  or "")
            info["iterator"]  = str(row.iterator  or "")

            if row.referenceFormulation:
                info["referenceFormulation"] = self.get_qname(row.referenceFormulation)
                rf_upper = info["referenceFormulation"].upper()
                # Map the reference formulation keyword to a simplified kind label.
                for key in ("CSV", "JSON", "XML", "XPATH", "SQL"):
                    if key in rf_upper:
                        # XPATH is treated as XML for display purposes.
                        info["kind"] = "XML" if key == "XPATH" else key

            # A table name or SQL query always implies an SQL source,
            # regardless of what the reference formulation says.
            if info["tableName"] or info["sqlQuery"]:
                info["kind"] = "SQL"

        return info

    # ------------------------------------------------------------------
    # Term map parsing
    # ------------------------------------------------------------------

    def parse_term_map_query(self, node_uri) -> dict:
        """
        Analyse a single term-map node and return a normalised descriptor.

        Returns a dict with:

        ``mapType``
            One of ``"constant"``, ``"template"``, ``"reference"``,
            or ``"other"``.
        ``raw_value``
            The underlying string value exactly as stored in the graph.
        ``value``
            The display-friendly form (CURIE for URIs, or the raw string).
        ``termTypeIRI``
            ``True`` when the term type is ``rr:IRI``.
        ``linkable``
            ``True`` when *value* can be turned into a hyperlink.
        ``href``
            The resolved full URI to link to, or ``None``.
        """
        result = {
            "mapType":     "other",
            "raw_value":   str(node_uri),
            "value":       self.get_qname(node_uri),
            "termTypeIRI": False,
        }

        for row in self.graph.query(term_map_info(), initBindings={"map": node_uri}):
            # Determine which kind of term map this is and store its value.
            if row.constant:
                result.update({
                    "mapType":   "constant",
                    "raw_value": str(row.constant),
                    "value":     self.get_qname(row.constant),
                })
            elif row.template:
                result.update({
                    "mapType":   "template",
                    "raw_value": str(row.template),
                    "value":     str(row.template),
                })
            elif row.reference:
                result.update({
                    "mapType":   "reference",
                    "raw_value": str(row.reference),
                    "value":     str(row.reference),
                })

            # Flag IRI term type so callers can distinguish IRIs from literals.
            if row.termType and str(row.termType).endswith("IRI"):
                result["termTypeIRI"] = True

        # Normalise rdf:type to the Turtle shorthand "a" for readability.
        if result["value"] == "rdf:type" or result["raw_value"] == _RDF_TYPE_URI:
            result["value"] = "a"

        val_str = str(result["value"])
        has_brackets = "{" in val_str and "}" in val_str

        # A value is linkable when it looks like a known term (CURIE, "a",
        # or constant URI) and does not contain template placeholders.
        result["linkable"] = (
            result["mapType"] == "constant" or ":" in val_str or val_str == "a"
        ) and not has_brackets

        # Resolve the href: rdf:type always links to its canonical URI;
        # everything else is expanded from its CURIE or taken as-is.
        result["href"] = (
            _RDF_TYPE_URI
            if val_str == "a"
            else (self.expand_curie(val_str) or result["raw_value"])
        ) if result["linkable"] else None

        return result

    # ------------------------------------------------------------------
    # Predicate–object map parsing
    # ------------------------------------------------------------------

    def get_predicates_info(self, tm_uri) -> list:
        """
        Return all predicate–object pairs defined for the triples map at
        *tm_uri* as a list of dicts.

        Each dict has:

        ``p``            – display form of the predicate CURIE (``"a"`` for rdf:type).
        ``p_href``       – raw predicate URI (always linkable).
        ``p_linkable``   – always ``True`` for predicates.
        ``o_display``    – human-readable object value.
        ``o_raw``        – raw object string.
        ``o_href``       – full URI for the object (``None`` if not linkable).
        ``o_linkable``   – whether the object can be rendered as a link.
        """
        predicates = []

        for row in self.graph.query(pom_info_query(tm_uri)):

            # --- Predicate display form ---
            p_raw    = str(row.p)
            p_qname  = self.get_qname(row.p)
            # Use "a" shorthand instead of the full rdf:type CURIE.
            p_display = "a" if (p_qname == "rdf:type" or p_raw == _RDF_TYPE_URI) else p_qname

            # --- Object display form and link resolution ---
            o_data = {"value": "", "raw_value": "", "href": None, "linkable": False}

            raw_obj          = row.constant or row.template or row.reference or ""
            o_data["raw_value"] = str(raw_obj)

            if row.constant:
                # Constants are compressed to their CURIE form.
                o_data["value"] = self.get_qname(row.constant)
            elif row.reference:
                # References are wrapped in curly braces to signal a field reference.
                o_data["value"] = "{" + str(raw_obj) + "}"
            else:
                o_data["value"] = str(raw_obj)

            val_str = str(o_data["value"])

            if row.constant and "{" not in val_str:
                raw_str  = str(raw_obj)
                expanded = None if raw_str.startswith("http") else self.expand_curie(o_data["value"])
                is_url   = raw_str.startswith("http")
                is_curie = expanded is not None

                # Link to the full URI if the constant is a URL or a known CURIE.
                # Plain literals (e.g. "EUR") stay non-linkable.
                if is_url or is_curie:
                    o_data.update({
                        "linkable": True,
                        "href":     raw_str if is_url else expanded,
                    })

            elif ":" in val_str and "{" not in val_str and not row.reference:
                # Looks like an un-flagged CURIE — try to resolve it.
                o_data.update({
                    "linkable": True,
                    "href":     self.expand_curie(val_str) or str(raw_obj),
                })

            predicates.append({
                "p":          p_display,
                "p_href":     p_raw,
                "p_linkable": True,
                "o_display":  o_data["value"],
                "o_raw":      o_data["raw_value"],
                "o_href":     o_data["href"],
                "o_linkable": o_data["linkable"],
            })

        return predicates

    # ------------------------------------------------------------------
    # Triples-map assembly
    # ------------------------------------------------------------------

    def build_triples_maps(self) -> list:
        """
        Build and return a list of structured triples-map descriptors,
        sorted alphabetically by their short identifier.

        Each entry is a dict with:

        ``id``               – short name derived from the triples-map URI.
        ``source_info``      – result of :meth:`parse_logical_source`.
        ``subject``          – display form of the subject map value.
        ``subject_raw``      – raw subject template string.
        ``subject_href``     – resolved URI for the subject (or ``None``).
        ``subject_linkable`` – whether the subject can be rendered as a link.
        ``predicates``       – list from :meth:`get_predicates_info`.
        ``joins``            – list from :meth:`get_join_conditions`.
        ``graph``            – named graph label(s) from :meth:`get_named_graph`.
        """
        # Collect the set of unique triples-map URIs from the graph.
        tm_uris = {
            tp.asdict()["triplesMap"].toPython()
            for tp in self.graph.query(triples_map_query)
        }

        results = []
        for tm in tm_uris:
            source_info  = self.parse_logical_source(tm)
            s_map_res    = list(self.graph.query(subject_map(tm)))

            # Skip triples maps that have no subject map defined.
            if not s_map_res:
                continue

            s_node       = s_map_res[0].subjectMap
            subject_info = self.parse_term_map_query(s_node)
            is_template  = "{" in str(s_map_res[0].template)

            results.append({
                "id":               self.get_id_from_tm(tm),
                "source_info":      source_info,
                # Use the template string verbatim when it contains placeholders;
                # otherwise use the compressed CURIE form.
                "subject":          str(s_map_res[0].template) if is_template else subject_info["value"],
                "subject_raw":      str(s_map_res[0].template),
                "subject_href":     subject_info.get("href"),
                "subject_linkable": subject_info.get("linkable"),
                "predicates":       self.get_predicates_info(tm),
                "joins":            self.get_join_conditions(tm),
                "graph":            self.get_named_graph(tm),
            })

        return sorted(results, key=lambda x: x["id"])

    # ------------------------------------------------------------------
    # Join condition parsing
    # ------------------------------------------------------------------

    def get_join_conditions(self, tm_uri) -> list:
        """
        Return all ``rr:joinCondition`` entries for the triples map at
        *tm_uri* as a list of dicts.

        Each dict contains:

        ``parent_tm``    – short ID of the parent triples map.
        ``child``        – child join key (source column/field).
        ``parent``       – parent join key (target column/field).
        ``s_template``   – subject template of the current (child) map.
        ``o_template``   – subject template of the parent map.
        ``predicate``    – CURIE of the linking predicate (``"a"`` for rdf:type).
        ``container_id`` – unique DOM-safe ID for embedding in HTML.
        """
        joins = []
        for i, row in enumerate(self.graph.query(join_condition(tm_uri))):
            parent_tm    = str(row.parentTriplesMap) if row.parentTriplesMap else ""
            parent_tm_id = self.get_id_from_tm(parent_tm)

            # Build a unique, DOM-safe identifier for this join container.
            source_id    = self.safe_id(self.get_id_from_tm(tm_uri))
            target_id    = self.safe_id(parent_tm_id)
            container_id = f"cy_join_{source_id}_{target_id}_{i}"

            s_template = str(row.s_template) if row.s_template else self.get_id_from_tm(tm_uri)
            o_template = str(row.o_template) if row.o_template else parent_tm_id

            # Compress the predicate URI to its CURIE form for readability;
            # normalise rdf:type to "a".
            if row.predicate:
                p_qname   = self.get_qname(row.predicate)
                predicate = (
                    "a"
                    if p_qname == "rdf:type" or str(row.predicate) == _RDF_TYPE_URI
                    else p_qname
                )
            else:
                predicate = ""

            joins.append({
                "parent_tm":    parent_tm_id,
                "child":        str(row.child)  if row.child  else "unknown",
                "parent":       str(row.parent) if row.parent else "unknown",
                "s_template":   s_template,
                "o_template":   o_template,
                "predicate":    predicate,
                "container_id": container_id,
            })

        return joins

    # ------------------------------------------------------------------
    # Named graph extraction
    # ------------------------------------------------------------------

    def get_named_graph(self, tm_uri) -> Optional[str]:
        """
        Return a comma-separated string of named-graph CURIEs for the
        triples map at *tm_uri*, or ``None`` if no named graph is declared.
        """
        graphs = []
        for row in self.graph.query(named_graph(tm_uri)):
            if row.graph:
                graphs.append(self.get_qname(row.graph))

        return ", ".join(graphs) if graphs else None