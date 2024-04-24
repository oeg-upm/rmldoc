

   
# GTFS-Madrid-Bench CSV mapping excerpt
   
   
**Version:**

* 0.1.0
   
**Authors**:

    
* Jhon Toledo
   
    
* Ana Iglesias-Molina
   

**Mapping file:**
example_input.ttl

**Description**: RML mapping with a subset of the GTFS-Madrid-Bench mapping for CSV files.


**Date created**: 03-05-2024

**License**:

[![http://insertlicenseURIhere.org](https://img.shields.io/badge/License-Creative%20Commons%20Attribution%204.0%20International%20(CC%20BY%204.0)-blue.svg)](https://creativecommons.org/licenses/by/4.0/)



------


## **Namespaces used in the document**

| Prefix       |               IRI                   |
| :----------- | :----------------------------------  |
| gtfs     | http://vocab.gtfs.org/terms# |



## Mappings
>[!NOTE]
>1. **Source**: This is where you define the source of your data, which can be a relational database, a CSV file, or any other structured data source. The logical source specifies the location and format of your source data.
>2. **Subject**: This part of the mapping defines how the data from the logical source will be used to create RDF subjects, typically using templates and column mappings.
>3. **Predicate Object**: These describe how the data from the logical source will be used to generate RDF triples, indicating relationships between subjects and objects.
>4. **JoinCondition**: is used to specify the conditions under which two data sources or tables should be joined when creating RDF triples through mappings.


## frequencies
- **Source**

```bash
/data/FREQUENCIES.csv
``` 
- **Subject**
```bash
http://transport.linkeddata.es/madrid/metro/frequency/{trip_id}-{start_time}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| a | gtfs:Frequency |
| gtfs:startTime | {start_time} |
| gtfs:endTime | {end_time} |
| gtfs:headwaySeconds | {headway_secs} |
| gtfs:exactTimes | {exact_times} |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://transport.linkeddata.es/madrid/metro/frequency/{trip_id}-{start_time}"] -->|"a"| object1("gtfs:Frequency")
S["http://transport.linkeddata.es/madrid/metro/frequency/{trip_id}-{start_time}"] -->|"gtfs:startTime"| object2("{start_time}")
S["http://transport.linkeddata.es/madrid/metro/frequency/{trip_id}-{start_time}"] -->|"gtfs:endTime"| object3("{end_time}")
S["http://transport.linkeddata.es/madrid/metro/frequency/{trip_id}-{start_time}"] -->|"gtfs:headwaySeconds"| object4("{headway_secs}")
S["http://transport.linkeddata.es/madrid/metro/frequency/{trip_id}-{start_time}"] -->|"gtfs:exactTimes"| object5("{exact_times}")
    
``` 


- **Join Condition**:
    - Source triples map: **frequencies**
    - Target triples map: **trips**
    - Function: **equal(trip_id, trip_id)**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S1["http://transport.linkeddata.es/madrid/metro/frequency/{trip_id}-{start_time}"] -->|"gtfs:trip"| object1("http://transport.linkeddata.es/madrid/metro/trips/{trip_id}")

``` 

 ## trips
- **Source**

```bash
/data/TRIPS.csv
``` 
- **Subject**
```bash
http://transport.linkeddata.es/madrid/metro/trips/{trip_id}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| a | gtfs:Trip |
| gtfs:headsign | {trip_headsign} |
| gtfs:shortName | {trip_short_name} |
| gtfs:direction | {direction_id} |
| gtfs:block | {block_id} |
| gtfs:wheelchairAccessible | http://transport.linkeddata.es/resource/WheelchairBoardingStatus/{wheelchair_accessible} |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://transport.linkeddata.es/madrid/metro/trips/{trip_id}"] -->|"a"| object1("gtfs:Trip")
S["http://transport.linkeddata.es/madrid/metro/trips/{trip_id}"] -->|"gtfs:headsign"| object2("{trip_headsign}")
S["http://transport.linkeddata.es/madrid/metro/trips/{trip_id}"] -->|"gtfs:shortName"| object3("{trip_short_name}")
S["http://transport.linkeddata.es/madrid/metro/trips/{trip_id}"] -->|"gtfs:direction"| object4("{direction_id}")
S["http://transport.linkeddata.es/madrid/metro/trips/{trip_id}"] -->|"gtfs:block"| object5("{block_id}")
S["http://transport.linkeddata.es/madrid/metro/trips/{trip_id}"] -->|"gtfs:wheelchairAccessible"| object6("http://transport.linkeddata.es/resource/WheelchairBoardingStatus/{wheelchair_accessible}")
    
``` 




----

**This documentation was generated using**  *[RMLdoc](https://oeg-upm.github.io/rmldoc/)*.
