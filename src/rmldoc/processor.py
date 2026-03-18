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
# Namespaces
# ---------------------------------------------------------------------------
RR = Namespace("http://www.w3.org/ns/r2rml#")
RML = Namespace("http://semweb.mmlab.be/ns/rml#")
RDFNS = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
SCHEMA = Namespace("http://schema.org/")
DCT = Namespace("http://purl.org/dc/terms/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
QL = Namespace("http://semweb.mmlab.be/ns/ql#")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_RDF_TYPE_URI = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"


class RMLDocProcessor:
    """Processor class to handle RML mapping files and extract RDF metadata."""

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self, mapping_path: Path):
        self.mapping_path = mapping_path
        self.graph = self._load_graph(mapping_path)
        self.prefix_map = self._get_custom_prefixes()

    def _load_graph(self, mapping_path: Path) -> Graph:
        graph = Graph()
        graph.parse(location=str(mapping_path), format="turtle")

        # Register prefixes so get_qname returns e.g. 'esdir:DireccionPostal'
        # instead of the full URL.
        for prefix, uri in graph.namespaces():
            graph.namespace_manager.bind(prefix, uri, override=True)

        return graph

    # ------------------------------------------------------------------
    # Helpers — identifiers & prefixes
    # ------------------------------------------------------------------

    @staticmethod
    def safe_id(s: str) -> str:
        return re.sub(r"[^A-Za-z0-9_]", "_", s)

    @staticmethod
    def get_id_from_tm(tm: str) -> str:
        return tm.rstrip("/").rsplit("/", 1)[-1]

    def _get_custom_prefixes(self) -> dict:
        default_prefixes = dict(Graph().namespaces()).keys()
        return {
            prefix: str(uri)
            for prefix, uri in self.graph.namespaces()
            if prefix and prefix not in default_prefixes
        }

    # ------------------------------------------------------------------
    # Helpers — graph access
    # ------------------------------------------------------------------

    def get_first_obj(self, subject: Any, predicate: Any) -> Optional[Any]:
        return next(self.graph.objects(subject, predicate), None)

    def get_qname(self, term: Any) -> str:
        if term is None:
            return ""
        if isinstance(term, Literal):
            return str(term)
        try:
            return self.graph.namespace_manager.normalizeUri(term)
        except Exception:
            return str(term)

    def expand_curie(self, value: str) -> Optional[str]:
        try:
            return str(self.graph.namespace_manager.expand_curie(value))
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    def extract_mapping_metadata(self) -> dict:
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
            "version": str(self.get_first_obj(ds_node, SCHEMA.version) or "0.0.0"),
            "date_created": str(self.get_first_obj(ds_node, SCHEMA.dateCreated) or ""),
            "description": str(self.get_first_obj(ds_node, SCHEMA.description) or ""),
            "license_url": str(
                self.get_first_obj(ds_node, SCHEMA.license)
                or self.get_first_obj(ds_node, DCT.license)
                or ""
            ),
            "authors": [],
            "mapping_filename": self.mapping_path.name,
            "yarrrml_file": self.mapping_path.with_suffix(".yml").name,
        }

        if ds_node:
            for person in self.graph.objects(ds_node, SCHEMA.contributor):
                name = str(self.get_first_obj(person, RDFS.label) or "")
                mbox = self.get_first_obj(person, FOAF.mbox)
                if name:
                    meta["authors"].append({"name": name, "mbox": str(mbox) if mbox else ""})

        return meta

    # ------------------------------------------------------------------
    # Logical source
    # ------------------------------------------------------------------

    def parse_logical_source(self, tm_uri) -> dict:
        info = {
            "kind": "Other",
            "source": "",
            "referenceFormulation": "",
            "iterator": "",
            "sqlQuery": "",
            "tableName": "",
        }

        for row in self.graph.query(logical_source_info(tm_uri)):
            info["source"] = str(row.source or "")
            info["tableName"] = str(row.tableName or "")
            info["sqlQuery"] = str(row.sqlQuery or "")
            info["iterator"] = str(row.iterator or "")

            if row.referenceFormulation:
                info["referenceFormulation"] = self.get_qname(row.referenceFormulation)
                rf_upper = info["referenceFormulation"].upper()
                for key in ("CSV", "JSON", "XML", "XPATH", "SQL"):
                    if key in rf_upper:
                        info["kind"] = "XML" if key == "XPATH" else key

            if info["tableName"] or info["sqlQuery"]:
                info["kind"] = "SQL"

        return info

    # ------------------------------------------------------------------
    # Term maps
    # ------------------------------------------------------------------

    def parse_term_map_query(self, node_uri) -> dict:
        result = {
            "mapType": "other",
            "raw_value": str(node_uri),
            "value": self.get_qname(node_uri),
            "termTypeIRI": False,
        }

        for row in self.graph.query(term_map_info(), initBindings={"map": node_uri}):
            if row.constant:
                result.update({
                    "mapType": "constant",
                    "raw_value": str(row.constant),
                    "value": self.get_qname(row.constant),
                })
            elif row.template:
                result.update({
                    "mapType": "template",
                    "raw_value": str(row.template),
                    "value": str(row.template),
                })
            elif row.reference:
                result.update({
                    "mapType": "reference",
                    "raw_value": str(row.reference),
                    "value": str(row.reference),
                })

            if row.termType and str(row.termType).endswith("IRI"):
                result["termTypeIRI"] = True

        # Normalise rdf:type → 'a'
        if result["value"] == "rdf:type" or result["raw_value"] == _RDF_TYPE_URI:
            result["value"] = "a"

        val_str = str(result["value"])
        has_brackets = "{" in val_str and "}" in val_str
        result["linkable"] = (
                                     result["mapType"] == "constant" or ":" in val_str or val_str == "a"
                             ) and not has_brackets

        result["href"] = (
            _RDF_TYPE_URI
            if val_str == "a"
            else (self.expand_curie(val_str) or result["raw_value"])
        ) if result["linkable"] else None

        return result

    # ------------------------------------------------------------------
    # Predicates
    # ------------------------------------------------------------------

    def get_predicates_info(self, tm_uri) -> list:
        predicates = []

        for row in self.graph.query(pom_info_query(tm_uri)):
            # --- Predicate ---
            p_raw = str(row.p)
            p_qname = self.get_qname(row.p)
            p_display = "a" if (p_qname == "rdf:type" or p_raw == _RDF_TYPE_URI) else p_qname

            # --- Object ---
            o_data = {"value": "", "raw_value": "", "href": None, "linkable": False}
            raw_obj = row.constant or row.template or row.reference or ""
            o_data["raw_value"] = str(raw_obj)
            #o_data["value"] = self.get_qname(row.constant) if row.constant else str(raw_obj)
            if row.constant:
                o_data["value"] = self.get_qname(row.constant)
            elif row.reference:
                o_data["value"] = "{" + str(raw_obj) + "}"  # ← llaves añadidas
            else:
                o_data["value"] = str(raw_obj)

            val_str = str(o_data["value"])
            if row.constant and "{" not in val_str:
                raw_str = str(raw_obj)
                expanded = None if raw_str.startswith("http") else self.expand_curie(o_data["value"])
                is_url = raw_str.startswith("http")
                is_curie = expanded is not None
                if is_url or is_curie:
                    o_data.update({
                        "linkable": True,
                        "href": raw_str if is_url else expanded,
                    })
                # Plain literals (e.g. "EUR") stay non-linkable with no href.
            elif ":" in val_str and "{" not in val_str and not row.reference:
                o_data.update({
                    "linkable": True,
                    "href": self.expand_curie(val_str) or str(raw_obj),
                })


            predicates.append({
                "p": p_display,
                "p_href": p_raw,
                "p_linkable": True,
                "o_display": o_data["value"],
                "o_raw": o_data["raw_value"],
                "o_href": o_data["href"],
                "o_linkable": o_data["linkable"],
            })

        return predicates

    # ------------------------------------------------------------------
    # Triples maps
    # ------------------------------------------------------------------

    def build_triples_maps(self) -> list:
        tm_uris = {
            tp.asdict()["triplesMap"].toPython()
            for tp in self.graph.query(triples_map_query)
        }

        results = []
        for tm in tm_uris:
            source_info = self.parse_logical_source(tm)
            s_map_res = list(self.graph.query(subject_map(tm)))

            if not s_map_res:
                continue

            s_node = s_map_res[0].subjectMap
            subject_info = self.parse_term_map_query(s_node)
            is_template = "{" in str(s_map_res[0].template)

            results.append({
                "id": self.get_id_from_tm(tm),
                "source_info": source_info,
                "subject": str(s_map_res[0].template) if is_template else subject_info["value"],
                "subject_raw": str(s_map_res[0].template),
                "subject_href": subject_info.get("href"),
                "subject_linkable": subject_info.get("linkable"),
                "predicates": self.get_predicates_info(tm),
                "joins": self.get_join_conditions(tm),
                "graph": self.get_named_graph(tm),
            })

        return sorted(results, key=lambda x: x["id"])

    # ------------------------------------------------------------------
    # Joins
    # ------------------------------------------------------------------

    def get_join_conditions(self, tm_uri) -> list:
        joins = []
        for i, row in enumerate(self.graph.query(join_condition(tm_uri))):
            parent_tm = str(row.parentTriplesMap) if row.parentTriplesMap else ""
            parent_tm_id = self.get_id_from_tm(parent_tm)

            source_id = self.safe_id(self.get_id_from_tm(tm_uri))
            target_id = self.safe_id(parent_tm_id)
            container_id = f"cy_join_{source_id}_{target_id}_{i}"

            s_template = str(row.s_template) if row.s_template else self.get_id_from_tm(tm_uri)
            o_template = str(row.o_template) if row.o_template else parent_tm_id

            # --- CAMBIO AQUÍ ---
            # Usamos self.get_qname() para que formatee el predicado como gtfs:trip
            if row.predicate:
                p_qname = self.get_qname(row.predicate)
                # Opcional: si el predicado es rdf:type, lo mostramos como 'a' igual que en los triples normales
                predicate = "a" if p_qname == "rdf:type" or str(row.predicate) == _RDF_TYPE_URI else p_qname
            else:
                predicate = ""
            # -------------------

            joins.append({
                "parent_tm": parent_tm_id,
                "child": str(row.child) if row.child else "unknown",
                "parent": str(row.parent) if row.parent else "unknown",
                "s_template": s_template,
                "o_template": o_template,
                "predicate": predicate,
                "container_id": container_id
            })
        return joins

    # ------------------------------------------------------------------
    # Named Graph
    # ------------------------------------------------------------------

    def get_named_graph(self, tm_uri) -> Optional[str]:
        graphs = []
        for row in self.graph.query(named_graph(tm_uri)):
            if row.graph:
                graphs.append(self.get_qname(row.graph))

        return ", ".join(graphs) if graphs else None