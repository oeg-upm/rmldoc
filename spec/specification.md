# RML Mapping Documentation (RMLdoc) Specification Document-Draft
**Version:** 0.1.0
**Date:** 2023-10-03

## Table of Contents

1. [Introduction](#introduction)
   - [Purpose](#purpose)
   - [Scope](#scope)
2. [Workflow](#workflow)
5. [Design Specifications](#design-specifications)
   - [Version](#version)
   - [Author](#author)
   - [License](#license)
   - [Namespaces](#namespaces)
   - [Source](#source)
   - [Subject](#subject)
   - [Predicate object](#predicate-object)
   - [Example](#Example)

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

### 1.1 Purpose

The purpose of RDF mapping documentation (RMD) is to provide a clear and comprehensive documentation of the [RDF mapping languages (RML)](https://rml.io/specs/rml/) within the RDF knowledge graph construction process.


### 1.2 Scope

The following table details which annotations are supported by this version of RDF Mapping Documentation (RMD).

| annotation-level | metadata | Description |
| ---------------- | -------------- | ----------- |
| mapping          | dc:contributor(**creator**?) |             |
| mapping    | rdfs:label     | be changed? |
| mapping | **ex:versionIRI** | **//ToDo** |
| TriplesMap       | rdfs:label     | **//ToDo**  be changed? |
| TriplesMap       | rdfs:comment |             |
| TriplesMap | **¿rmd:example?** | **//ToDo** |
| logicalSource | rdfs:label |             |
| logicalSource | rdfs:comment |             |
| subjectMap | rdfs:label |             |
| subjectMap | rdfs:comment |             |
| predicateObjectMap | rdfs:label |             |
| predicateObjectMap | rdfs:comment |             |
| predicateMap | rdfs:label |             |
| predicateMap | rdfs:comment | |
| objectMap | rdfs:label | |
| objectMap | rdfs:comment | |
| joinCondition | rdfs:label | |
| joinCondition | rdfs:comment | |

## 2. Workflow
[Include diagrams]

## 3. Design Specifications

Specifications for RDF Mapping documentation(RMD) detail how the RML mapping needs to be structured in order to show that information in the documentation. Here are some design specifications for RML Mapping.

### 3.1 Version: 
---
Input: 

```turtle
@prefix ns0: <https://w3id.org/mapping/gtfs/core#> .
<https://w3id.org/mapping/gtfs/core#> ns0:versionIRI <https://w3id.org/mapping/gtfs/csv/0.1.0> .
```
Output: 

**Version:**

https://w3id.org/mapping/gtfs/csv/0.1.0

---

### 3.2 Author: 

---
Input: 

```turtle
 <http://mapping.example.com/person>
  dc:contributor foaf:Person ;
  rdfs:label "John Doe" ;
  foaf:mbox <mailto:john@doe.com> .
```
Output: 

**Authors**:

* [John Doe](John_Doe@upm.es)

---

### 3.3 License:

---
Input: 

```turtle
 
```
Output: 

**License**:

[![httpinsertlicenseURIhereorg](https://img.shields.io/badge/License-Creative%20Commons%20Attribution%204.0%20International%20(CC%20BY%204.0)-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

---

### 3.4 Namespaces
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

### 3.5 Source
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

**Source**

| Feature | Value                |
| ------- | -------------------- |
| sources | /data/STOP_TIMES.csv |

---

### 3.6 Subject
---
Input: 

```turtle
	rr:subjectMap [
		a rr:SubjectMap;
		rr:template "http://transport.linkeddata.es/madrid/metro/trips/{trip_id}";
	];
```
Output: 

**Subject**

| URI                                                         |
| ----------------------------------------------------------- |
| http://transport.linkeddata.es/madrid/metro/trips/{trip_id} |

---

### 3.7 Predicate object
---
Input: 

```turtle
predicateObjectMap-->//ToDo
```
Output: 

| Property              | Collation¿?                                                  | param1  | param2  | condition |
| --------------------- | ------------------------------------------------------------ | ------- | ------- | --------- |
| a                     | gtfs:StopTime                                                |         |         |           |
| gtfs:arrivalTime      | arrival_time                                                 |         |         |           |
| gtfs:departureTime    | departure_time                                               |         |         |           |
| gtfs:stopSequence     | stop_sequence                                                |         |         |           |
| gtfs:headsign         | stop_headsign                                                |         |         |           |
| gtfs:pickupType       | http://transport.linkeddata.es/resource/PickupType/$(pickup_type) |         |         |           |
| gtfs:dropOffType      | http://transport.linkeddata.es/resource/DropOffType/$(drop_off_type) |         |         |           |
| gtfs:distanceTraveled | shape_dist_traveled                                          |         |         |           |
| gtfs:trip             | [trips](http://localhost:63342/markdownPreview/186959714/markdown-preview-index-437576200.html?_ijt=96for37v156vnbqmnn0othvpjg##trips) | trip_id | trip_id | equal     |
| gtfs:stop             | [stops](http://localhost:63342/markdownPreview/186959714/markdown-preview-index-437576200.html?_ijt=96for37v156vnbqmnn0othvpjg##trips) | stop_id | stop_id | equal     |

---

### 3.8 Example
---
Input: 

```turtle

```
Output: 

<details>
  <summary>RML example</summary>

  ```rdf
<stoptimes_0> a rr:TriplesMap;

	rml:logicalSource [
		a rml:LogicalSource;
		rml:source "/data/STOP_TIMES.csv";
		rml:referenceFormulation ql:CSV
	];
	rr:subjectMap [
		a rr:SubjectMap;
		rr:template "http://transport.linkeddata.es/madrid/metro/stoptimes/{trip_id}-{stop_id}-{arrival_time}";
	];
	rr:predicateObjectMap [
		rr:predicateMap [
			a rr:PredicateMap;
			rr:constant rdf:type;
		];
		rr:objectMap [
			a rr:ObjectMap;
			rr:constant gtfs:StopTime;
		];
	].
  ```
</details>

---

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