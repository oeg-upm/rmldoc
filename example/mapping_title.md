

   
# GTFS-Madrid-Bench CSV mapping
   
   
**Version:**

* 0.1.0
   
**Authors**:

    
* Jhon Toledo
   
    
* Ana Iglesias-Molina
   

**Mapping file:**
mapping_title.ttl


**License**:

[![http://insertlicenseURIhere.org](https://img.shields.io/badge/License-Creative%20Commons%20Attribution%204.0%20International%20(CC%20BY%204.0)-blue.svg)](https://creativecommons.org/licenses/by/4.0/)



------


## **Namespaces used in the document**

| Prefix       |               IRI.                   |
| :----------- | :----------------------------------  |
| schema1     | http://schema.org/ |
| gtfs     | http://vocab.gtfs.org/terms# |
| map     | http://mapping.example.com/ |
| ql     | http://semweb.mmlab.be/ns/ql# |
| dct     | http://purl.org/dc/terms/ |
| sd     | http://www.w3.org/ns/sparql-service-description# |
| rev     | http://purl.org/stuff/rev# |
| ma     | http://www.w3.org/ns/ma-ont# |
| rml     | http://semweb.mmlab.be/ns/rml# |
| geo1     | http://www.w3.org/2003/01/geo/wgs84_pos# |
| v     | http://rdf.data-vocabulary.org/# |
| rr     | http://www.w3.org/ns/r2rml# |



## Mappings
>[!NOTE]
>1. **Source**: This is where you define the source of your data, which can be a relational database, a CSV file, or any other structured data source. The logical source specifies the location and format of your source data.
>2. **Subject**: This part of the mapping defines how the data from the logical source will be used to create RDF subjects, typically using templates and column mappings.
>3. **Predicate Object**: These describe how the data from the logical source will be used to generate RDF triples, indicating relationships between subjects and objects.
>4. **JoinCondition**: is used to specify the conditions under which two data sources or tables should be joined when creating RDF triples through mappings.


## map_stoptimes_000
- **Source**

```bash
/data/STOP_TIMES.csv
``` 
- **Subject**
```bash
http://transport.linkeddata.es/madrid/metro/stoptimes/{trip_id}-{stop_id}-{arrival_time}
``` 
- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
| a | gtfs:StopTime |
| gtfs:arrivalTime | {arrival_time} |
- **RDF triples**
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%
flowchart LR
S["http://transport.linkeddata.es/madrid/metro/stoptimes/{trip_id}-{stop_id}-{arrival_time}"] -->|"a"| object1("gtfs:StopTime")
S["http://transport.linkeddata.es/madrid/metro/stoptimes/{trip_id}-{stop_id}-{arrival_time}"] -->|"gtfs:arrivalTime"| object2("{arrival_time}")
    
``` 




----

**This documentation was generated using**  *[RMLdoc](https://oeg-upm.github.io/rmldoc/)*.
