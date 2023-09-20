# RDF Mapping Documentation (RMD)

**Version:**

https://w3id.org/mapping/gtfs/csv/0.1.0

**Authors**:

* [John Doe1 ](John_Doe2@upm.es)
* [John Doe2](John_Doe2@upm.es)
* John Doe3
* **[John Doe4](https://github.com/jatoledo) - [ja.toledo@upm.es](mailto:ja.toledo@upm.es)**

**License**:

[![http://insertlicenseURIhere.org](https://img.shields.io/badge/License-Creative%20Commons%20Attribution%204.0%20International%20(CC%20BY%204.0)-blue.svg)](https://creativecommons.org/licenses/by/4.0/)



------




## **Namespaces used in the document** 

| Prefix | IRI.                                        |
| :----- | :------------------------------------------ |
| rr     | http://www.w3.org/ns/r2rml#                 |
| foaf   | http://xmlns.com/foaf/0.1/                  |
| xsd    | http://www.w3.org/2001/XMLSchema#           |
| rdfs   | http://www.w3.org/2000/01/rdf-schema#       |
| dc     | http://purl.org/dc/elements/1.1/            |
| rev    | http://purl.org/stuff/rev#                  |
| gtfs   | http://vocab.gtfs.org/terms#                |
| geo    | http://www.w3.org/2003/01/geo/wgs84_pos#    |
| schema | http://schema.org/                          |
| dct    | http://purl.org/dc/terms/                   |
| rml    | http://semweb.mmlab.be/ns/rml#              |
| ql     | http://semweb.mmlab.be/ns/ql#               |
| rdf    | http://www.w3.org/1999/02/22-rdf-syntax-ns# |

## stoptimes

### "Title 1"

"Lorem ipsum dolor .."

### [Source](https://rml.io/specs/rml/#logical-source)

| Feature | Value                        |
| ------- | ---------------------------- |
| sources | ['/data/STOP_TIMES.csv~csv'] |

### [Subject](https://rml.io/specs/rml/#subject-map)

| URI                                                          |
| ------------------------------------------------------------ |
| http://transport.linkeddata.es/madrid/metro/stoptimes/$(trip_id)-$(stop_id)-$(arrival_time) |

### [Predicate object](https://rml.io/specs/rml/#predicate-object-map)

| Property       |                Collation                |                param1                |                param2                |                condition                |
| :----------- | :----------------------------------  | -----------------------------------  | -----------------------------------  | -----------------------------------  |
| a     | gtfs:StopTime |  |  |  |
| gtfs:arrivalTime     | arrival_time                                                 |  |  |  |
| gtfs:departureTime     | departure_time |  |  |  |
| gtfs:stopSequence     | stop_sequence |  |  |  |
| gtfs:headsign     | stop_headsign |  |  |  |
| gtfs:pickupType     | http://transport.linkeddata.es/resource/PickupType/$(pickup_type) |  |  |  |
| gtfs:dropOffType     | http://transport.linkeddata.es/resource/DropOffType/$(drop_off_type) |  |  |  |
| gtfs:distanceTraveled     | shape_dist_traveled |  |  |  |
| gtfs:trip | [trips](##trips) | <span style="color:blue">trip_id</span> | <span style="color:blue">trip_id</span> | <span style="color:red">equal</span> |
| gtfs:stop | [stops](##trips) | <span style="color:blue">stop_id</span> | <span style="color:blue">stop_id</span> | <span style="color:red">equal</span> |

<details>
  <summary>RML example</summary>

  ```java
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





----

Copyright © 2023 Jhon Toledo Barreto | Universidad Politécnica de Madrid
