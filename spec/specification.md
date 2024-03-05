# RML Documentation (RMLdoc) Specification Document-Draft
**Version:** 0.1.0
**Date:** 2024-03-05

## Table of Contents

1. [Introduction](#introduction)
   - [Purpose](#purpose)
   - [Scope](#scope)
   
2. [Workflow](#workflow)

5. [Design Specifications](#design-specifications)
   
   - [Dataset](#dataset)
   
   - [Version](#version)
   
   - [Contributor](#contributor)
   
   - [License](#license)

   - [Namespaces](#namespaces)
   
   - [Source](#source)
   
   - [Subject](#subject)
   
   - [Predicate object](#predicate-object)
   
4. [Testing and Quality Assurance](#testing-and-quality-assurance)
- [Test Objectives](#test-objectives)
   
- [Test Environment](#test-environment)
   
- [Test Cases](#test-cases)


7. [Documentation References](#documentation-references)

8. [Appendix ](#appendix)

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

The purpose of RML documentation (RMLdoc) is to provide a clear and comprehensive documentation of the [RDF mapping languages (RML)](https://rml.io/specs/rml/) within the RDF knowledge graph construction process.
(COGE MAPPINGS EN TAL Y TAL LENGUAJE, PROCESA Y GENERA DOCUMENTACIÓN EN MD CON DIAGRAMAS IN HUMAN-READABLE WAY)




## 2. Workflow
[Include diagrams]
(COGER EL DIAGRAMA DEL PAPER Y EXPLICAR POR ENCIMA)
(PARA EL DIAGRAMA, FORMATO DE MAPPINGS DE ENTRADA Y VER SI SE PUEDE MEJORAR ALGO MAS)

## 3. Design Specifications

Specifications for **RML documentation(RMLdoc)** detail how the RML mapping needs to be structured in order to show that information in the documentation. Here are some design specifications for RML Mapping.

### 3.1 Metadata: 

(explicar que se cogen metadatos del mapping, se toma el documento como un void/schema:Dataset y tal y tal propiedades que vienen en la tabla)
The following table details which annotations are supported by this version of **RML Documentation (RMLdoc)**.
| annotation-level | metadata |
| ---------------- | -------------- |
| mapping | schema:Dataset |
| mapping          | schema:version |
| mapping | dc:contributor | schema:contributor |
| mapping    | schema:description |
| mapping | schema:contributor |
| mapping | schema:license |
| mapping | schema:title |

---

Input:  **schema:Dataset** (EJEMPLO CON TODOS LOS METADATOS QUE TIENEN LAS SIGUIENTES SUBSECCIONES PERO SOLO EN UNO)

```turtle
<http://mapping.example.com/rules_000>
  a schema:Dataset.
```

---



### X3.2 Version: 

---
Input: 

```turtle
<http://mapping.example.com/rules_000>
  schema:version "0.1.0" .
```
Output: 

**Version:**

- 0.1.0

---



### X3.3 Contributor: 

---
Input: 

```bash
http://mapping.example.com/person_000>
  dc:contributor foaf:Person ;
  rdfs:label "Jhon Toledo" .

<http://mapping.example.com/person_001>
  dc:contributor foaf:Person ;
  rdfs:label "Ana Iglesias-Molina" .
```
Output: 

**Authors**:

- Jhon Toledo
- Ana Iglesias-Molina

---



### X3.4 License:

---
Input: 

```turtle
 <http://mapping.example.com/rules_000>
  schema:license <https://github.com/oeg-upm/rmldoc/blob/main/LICENSE> .
```
Output: 

**License**:

https://github.com/oeg-upm/rmldoc/blob/main/LICENSE

Default output:


[![httpinsertlicenseURIhereorg](https://img.shields.io/badge/License-Creative%20Commons%20Attribution%204.0%20International%20(CC%20BY%204.0)-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

---



### X3.5 Namespaces

---
Input: 

```turtle
@prefix rr: <http://www.w3.org/ns/r2rml#>.
@prefix foaf: <http://xmlns.com/foaf/0.1/>.
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix dc: <http://purl.org/dc/elements/1.1/>.
@prefix rml: <http://semweb.mmlab.be/ns/rml#>.
```
Output: 

**Namespaces used in the document**

| Prefix | IRI.                                  |
| ------ | ------------------------------------- |
| rr     | http://www.w3.org/ns/r2rml#           |
| foaf   | http://xmlns.com/foaf/0.1/            |
| xsd    | http://www.w3.org/2001/XMLSchema#     |
| rdfs   | http://www.w3.org/2000/01/rdf-schema# |
| dc     | http://purl.org/dc/elements/1.1/      |
| rml    | http://semweb.mmlab.be/ns/rml#        |

---



### 3.2 Source

(QUÉ SE ESTÁ COGIENDO A NIVEL CONCPTUAL, REDIRECCIONAR A SPEC DE RML)

---
Input: 

```turtle
	rml:logicalSource [
		a rml:LogicalSource;
		rml:source "/data/STOP_TIMES.csv";
		rml:referenceFormulation ql:CSV
	];
```
Output: 

- **Source**

```
/data/STOP_TIMES.csv
```

---



### 3.3 Subject

---
Input: 

```turtle
	rr:subjectMap [
		a rr:SubjectMap;
		rr:template "http://transport.linkeddata.es/madrid/metro/trips/{trip_id}";
	];
```
Output: 

- **Subject**

```
http://transport.linkeddata.es/madrid/metro/trips/{trip_id}
```

---



### 3.4 Predicate-object

---
Input: 

```turtle
	rr:predicateObjectMap [
		rr:predicateMap [
			a rr:PredicateMap;
			rr:constant rdf:type;
		];
		rr:objectMap [
			a rr:ObjectMap;
			rr:constant <http://vocab.gtfs.org/terms#StopTime>;
		];
	];
	rr:predicateObjectMap [
		rr:predicateMap [
			a rr:PredicateMap;
			rr:constant gtfs:arrivalTime;
		];
		rr:objectMap [
			a rr:ObjectMap;
			rml:reference "arrival_time";
		];
```
Output: 

- **Predicate Object**

| Predicate        | Object         |
| :--------------- | :------------- |
| a                | gtfs:StopTime  |
| gtfs:arrivalTime | {arrival_time} |

---


(SI NO HAY TESTING ESTO NOS LO CARGAMOS) (FUTURE WORK)
## 4. Testing and Quality Assurance

### 4.1 Test Objectives
[Explain the objectives]

### 4.2 Test Environment
[Describe the testing environment]

### 4.3 Test Cases
[Use yarrrml-parser test](https://github.com/RMLio/yarrrml-parser/tree/development/test)

[Use RINF Mappings test]

[Use GTFS-Madrid-Bench mappings](https://github.com/oeg-upm/gtfs-bench/tree/master/mappings)

## 5. Documentation References
[references]

## 6. Appendix
[additional information]


Copyright © 2023 *[Ontology Engineering Group](https://oeg.fi.upm.es/)*, *[Universidad Politécnica de Madrid](https://www.upm.es/internacional)*.
