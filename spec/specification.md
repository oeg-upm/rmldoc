# RML Documentation (RMLdoc) Specification Document-Draft
**Version:** 0.1.0
**Date:** 2024-03-05

## Table of Contents

1. [Introduction](#1-introduction)
   - [Purpose](#purpose)
   - [Scope](#scope)
2. [Workflow](#workflow)
5. [Design Specifications](#design-specifications)
   - [Metadata](#metadata)
   - [RML visualization](#32-rml-visualization)
   
4. [Documentation References](#documentation-references)

## 1. Introduction

Mapping documentation, in the context of data integration and data management, refers to a set of documents and information that describe how data from one source or system is related or "mapped" to data in another source. The primary purpose of mapping documentation is to provide a clear understanding of how data is transformed, converted, or linked between different data formats.

**Objectives:**

The primary objectives of mapping documentation are as follows:

1. **Data Integration:** The primary objective is to generate clear documentation defining how data from one source relates to data in another. This ensures that data can be combined and used cohesively across different sources.
2. **Data Transformation:** Mapping documentation specifies how data values are transformed, converted, or translated between sources. 
3. **Data Quality:** By documenting mapping rules and validation criteria, mapping documentation helps maintain data quality by ensuring that data is validated and cleaned during the integration process.
4. **Interoperability:** Mapping documentation promotes interoperability between systems and data sources. It allows different knowledge graph engineers, researchers and stakeholders to understand and work with data in a consistent and standardized manner.
5. **Traceability:** Mapping documentation provides traceability, allowing users to trace data back to its source. This is important for troubleshooting, and data lineage analysis.
7. **Project Collaboration:** Mapping documentation serves as a communication tool among various stakeholders involved in a data integration project, including data analysts, data engineers, and business users. It helps ensure everyone is on the same page regarding data transformations and mappings.
8. **Change Management:** As data sources or requirements change over time, mapping documentation can be updated to reflect these changes, making it easier to manage and adapt to evolving data needs.

In summary, mapping documentation plays a critical role in ensuring data consistency, quality, and interoperability across different systems and data sources. It facilitates the effective use of data in various business processes and analytical activities.

### 1.1 Purpose and scope

**RML documentation (RMLdoc)** is a tool designed to simplify the process of generating documentation of mappings used for knowledge graph construction. It automates the documentation generation process, allowing users to easily understand the mapping transformation rules defined within their projects. Given an input mapping file written in R2RML, RML, or YARRRML, RMLdoc will generate a detailed Markdown documentation explaining each mapping with corresponding diagrams, in a human readable manner.


## 2. Workflow
**RMLdoc** is a tool designed to accept either [RML](https://rml.io/specs/rml/) or YARRRML files as input and generate comprehensive documentation. It leverages [rdflib](https://rdflib.readthedocs.io/en/stable/index.html) to manage mappings when processing turtle files, and extracting crucial details via SPARQL queries. This extracted data is then used to generate documentation utilizing a [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) template. Finally, **RMLdoc** generates markdown documentation of the mappings, aiding in better visualizing the relationship between the ontology and the data source.





![RMLdoc](../images/rmldoc-workflow.png)



## 3. Design Specifications

Specifications for **RML documentation(RMLdoc)** detail how the RML mapping needs to be structured in order to show that information in the documentation. Here are some design specifications for RML Mapping.

### 3.1 Metadata: 

**RML Documentation (RMLdoc)** accepts the following metadata within the RML mapping to generate the documentation. It will display the version, author, and license by default to promote the use of these metadata within the mappings.

| Metadata |  |  |
| -------------- | -------------- | -------------- |
| **schema:Dataset**\| **void:Dataset**\| **dcat:Dataset** | [schema:Dataset](https://schema.org/Dataset) | A collection of data |
| **schema:version**\| **dcat:version** | [schema:version](https://schema.org/version) | The version of the mapping. |
| **schema:author** | [schema:author](https://schema.org/author) | The author of this content. |
| **schema:contributor**\| **dc:contributor** | [schema:contributor](https://schema.org/contributor) | contributor to the mapping. |
| **schema:description**\| **dc:description** | [schema:description](https://schema.org/description) | A description of the item |
| **schema:license**\| **dc:license** | [schema:license](https://schema.org/license) | A license document that applies to this content, typically indicated by URL. |
| **schema:title**\| **dc:title** | [schema:title](https://schema.org/title) | The title of the mapping document |
| **schema:dateCreated**\| **dc:created** | [schema:dateCreated](https://schema.org/dateCreated) | The date on which the mapping was created |



---



### 3.2 RML visualization

**Source**: Specifies the location of the source data.

---

- **Source**

```
/data/FREQUENCIES.csv
```

---



**Subject**: Defines how the subject of the RDF triples should be generated

---

- **Subject**

```
http://transport.linkeddata.es/madrid/metro/frequency/{trip_id}-{start_time}
```


---



**Predicate Object**: Specifies how predicate-object pairs should be generated

---

- **Predicate Object**

| Predicate           | Object         |
| ------------------- | -------------- |
| a                   | gtfs:Frequency |
| gtfs:startTime      | {start_time}   |
| gtfs:endTime        | {end_time}     |
| gtfs:headwaySeconds | {headway_secs} |
| gtfs:exactTimes     | {exact_times}  |

---



**Join Condition:** Specifies the conditions for joining the child triples map with the parent triples map.

---

- **Join Condition**:
  - Source triples map: **frequencies**
  - Target triples map: **trips**
  - Function: **equal(trip_id, trip_id)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S1["http://transport.linkeddata.es/madrid/metro/frequency/{trip_id}-{start_time}"] -->|"gtfs:trip"| object1("http://transport.linkeddata.es/madrid/metro/trips/{trip_id}")


```

---



## 4. Documentation References

* https://rml.io/specs/rml/
* https://rml.io/yarrrml/spec/

----------------------------

Copyright © 2024 *[RMLdoc](https://github.com/oeg-upm/rmldoc)*
