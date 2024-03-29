# RDF Mapping Documentation (RMD)

**Version:**

**Authors**:

**License**:

[![http://insertlicenseURIhere.org](https://img.shields.io/badge/License-Creative%20Commons%20Attribution%204.0%20International%20(CC%20BY%204.0)-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

------


## **Namespaces used in the document**

| Prefix       |               IRI.                   |
| :----------- | :----------------------------------  |
| rr     | http://www.w3.org/ns/r2rml# |
| foaf     | http://xmlns.com/foaf/0.1/ |
| xsd     | http://www.w3.org/2001/XMLSchema# |
| rdfs     | http://www.w3.org/2000/01/rdf-schema# |
| dc     | http://purl.org/dc/elements/1.1/ |
| rev     | http://purl.org/stuff/rev# |
| gtfs     | http://vocab.gtfs.org/terms# |
| geo     | http://www.w3.org/2003/01/geo/wgs84_pos# |
| schema     | http://schema.org/ |
| dct     | http://purl.org/dc/terms/ |
| rml     | http://semweb.mmlab.be/ns/rml# |
| ql     | http://semweb.mmlab.be/ns/ql# |
| rdf     | http://www.w3.org/1999/02/22-rdf-syntax-ns# |


## mappings
>[!NOTE]
>
>1. **Source**: This is where you define the source of your data, which can be a relational database, a CSV file, or any other structured data source. The logical source specifies the location and format of your source data.
>2. **Subject**: This part of the mapping defines how the data from the logical source will be used to create RDF subjects, typically using templates and column mappings.
>3. **Predicate Object**: These describe how the data from the logical source will be used to generate RDF triples, indicating relationships between subjects and objects.


### stoptimes

- **Source**

```bash
['/data/STOP_TIMES.csv']
```

- **Subject**


```bash
http://transport.linkeddata.es/madrid/metro/stoptimes/$(trip_id)-$(stop_id)-$(arrival_time)
```

- **Predicate Object**

| Predicate          | Object            |
| :----------------- | :---------------- |
| gtfs:arrivalTime   | $(arrival_time)   |
| gtfs:departureTime | $(departure_time) |
| gtfs:trip          |                   |

- **The RDF triples generated**


```mermaid
%%{ init : { "theme" : "forest", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
	S["http://transport.linkeddata.es/madrid/metro/stoptimes/$(trip_id)-$(stop_id)-$(arrival_time)"] -->|"http://www.w3.org/1999/02/22-rdf-syntax-ns#type"| o0("http://vocab.gtfs.org/terms#StopTime")
    S["http://transport.linkeddata.es/madrid/metro/stoptimes/$(trip_id)-$(stop_id)-$(arrival_time)"] -->|"http://vocab.gtfs.org/terms#arrivalTime"| o1("$(arrival_time)")
	S["http://transport.linkeddata.es/madrid/metro/stoptimes/$(trip_id)-$(stop_id)-$(arrival_time)"] -->|"http://vocab.gtfs.org/terms#departureTime"| o2("$(departure_time)")
	S["http://transport.linkeddata.es/madrid/metro/stoptimes/$(trip_id)-$(stop_id)-$(arrival_time)"] -->|"http://vocab.gtfs.org/terms#stopSequence"| o3("$(stop_sequence)")
	S["http://transport.linkeddata.es/madrid/metro/stoptimes/$(trip_id)-$(stop_id)-$(arrival_time)"] -->|"http://vocab.gtfs.org/terms#headsign"| o4("$(stop_headsign)")
	S["http://transport.linkeddata.es/madrid/metro/stoptimes/$(trip_id)-$(stop_id)-$(arrival_time)"] -->|"http://vocab.gtfs.org/terms#pickupType"| o5("http://transport.linkeddata.es/resource/PickupType/$(pickup_type)")
	S["http://transport.linkeddata.es/madrid/metro/stoptimes/$(trip_id)-$(stop_id)-$(arrival_time)"] -->|"http://vocab.gtfs.org/terms#dropOffType"| o6("http://transport.linkeddata.es/resource/DropOffType/$(drop_off_type)")
	S["http://transport.linkeddata.es/madrid/metro/stoptimes/$(trip_id)-$(stop_id)-$(arrival_time)"] -->|"http://vocab.gtfs.org/terms#distanceTraveled"| o7("$(shape_dist_traveled)")
    
```

- **Function: equal**

```mermaid
%%{ init : { "theme" : "forest", "flowchart" : { "curve" : "linear" }}}%%
classDiagram
direction LR
stoptimes --> trip : equal
stoptimes --> stops : equal
stoptimes : trip_id
stoptimes : stop_id
trip:trip_id 
stops : stop_id

```

