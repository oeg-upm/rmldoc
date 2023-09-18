**Authors**:

Jhon Toledo [(Ontology Engienering Group - Universidad Politécnica de Madrid)](https://oeg.fi.upm.es/)

**License**:

[![http://insertlicenseURIhere.org](https://img.shields.io/badge/License-Creative%20Commons%20Attribution%204.0%20International%20(CC%20BY%204.0)-blue.svg)](http://insertlicenseurihere.org/)

# Namespaces used in the document



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



# mappings

The mappings collection

## stoptimes

### Titulo1

Lorem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el texto de relleno estándar de las industrias desde el año 1500, cuando un impresor (N. del T. persona que se dedica a la imprenta) desconocido usó una galería de textos y los mezcló de tal manera que logró hacer un libro de textos especimen. No sólo sobrevivió 500 años, sino que tambien ingresó como texto de relleno en documentos electrónicos, quedando esencialmente igual al original. Fue popularizado en los 60s con la creación de las hojas "Letraset", las cuales contenian pasajes de Lorem Ipsum, y más recientemente con software de autoedición, como por ejemplo Aldus PageMaker, el cual incluye versiones de Lorem Ipsum.



| Property       |                Column name                |                param1                |                param1                |                condition                |
| :----------- | :----------------------------------  | -----------------------------------  | -----------------------------------  | -----------------------------------  |
| a     | gtfs:StopTime |  |  |  |
| gtfs:arrivalTime     | arrival_time                                                 |  |  |  |
| gtfs:departureTime     | departure_time |  |  |  |
| gtfs:stopSequence     | stop_sequence |  |  |  |
| gtfs:headsign     | stop_headsign |  |  |  |
| gtfs:pickupType     | http://transport.linkeddata.es/resource/PickupType/$(**pickup_type**) |  |  |  |
| gtfs:dropOffType     | http://transport.linkeddata.es/resource/DropOffType/$(**drop_off_type**) |  |  |  |
| gtfs:distanceTraveled     | shape_dist_traveled |  |  |  |
| gtfs:trip | [trips](#trips) | <span style="color:blue">trip_id</span> | <span style="color:blue">trip_id</span> | <span style="color:red">equal</span> |
| gtfs:stop | [stops](#trips) | <span style="color:blue">stop_id</span> | <span style="color:blue">stop_id</span> | <span style="color:red">equal</span> |




























## trips
| Property       |                Collation.                   |
| :----------- | :----------------------------------  |
| a     | gtfs:Trip |
| gtfs:headsign     | $(trip_headsign) |
| gtfs:shortName     | $(trip_short_name) |
| gtfs:direction     | $(direction_id) |
| gtfs:block     | $(block_id) |
| gtfs:wheelchairAccessible     | http://transport.linkeddata.es/resource/WheelchairBoardingStatus/$(wheelchair_accessible)~iri |
| p     | o |
| p     | o |
| p     | o |




## routes
| Property       |                Collation.                   |
| :----------- | :----------------------------------  |
| a     | gtfs:Route |
| gtfs:shortName     | <span style="color:red">$(route_short_name)</span> |
| gtfs:longName     | $(route_long_name) |
| dct:description     | $(route_desc) |
| gtfs:routeType     | <span style="color:red">http://transport.linkeddata.es/resource/RouteType/$(route_type)~iri</span> |
| gtfs:routeUrl     | $(route_url)~iri |
| gtfs:color     | $(route_color) |
| gtfs:textColor     | $(route_text_color) |
| p     | o |




## agency
| Property       |                Collation.                   |
| :----------- | :----------------------------------  |
| a     | gtfs:Agency |
| foaf:page     | $(agency_url)~iri |
| foaf:name     | $(agency_name) |
| gtfs:timeZone     | $(agency_timezone) |
| dct:language     | $(agency_lang) |
| foaf:phone     | $(agency_phone) |
| gtfs:fareUrl     | $(agency_fare_url)~iri |




## stops
| Property       |                Collation.                   |
| :----------- | :----------------------------------  |
| a     | gtfs:Stop |
| gtfs:code     | $(stop_code) |
| dct:identifier     | $(stop_id) |
| foaf:name     | $(stop_name) |
| dct:description     | $(stop_desc) |
| geo:lat     | $(stop_lat) |
| geo:long     | $(stop_lon) |
| gtfs:zone     | $(zone_id) |
| foaf:page     | $(stop_url)~iri |
| gtfs:locationType     | http://transport.linkeddata.es/resource/LocationType/$(location_type)~iri |
| gtfs:timeZone     | $(stop_timezone) |
| gtfs:wheelchairAccessible     | http://transport.linkeddata.es/resource/WheelchairBoardingStatus/$(wheelchair_boarding)~iri |
| p     | o |




## services1
| Property       |                Collation.                   |
| :----------- | :----------------------------------  |
| a     | gtfs:Service |
| p     | o |




## services2
| Property       |                Collation.                   |
| :----------- | :----------------------------------  |
| a     | gtfs:Service |
| p     | o |




## calendar_date_rules
| Property       |                Collation.                   |
| :----------- | :----------------------------------  |
| a     | gtfs:CalendarDateRule |
| dct:date     | $(date) |
| gtfs:dateAddition     | $(exception_type) |




## calendar_rules
| Property       |                Collation.                   |
| :----------- | :----------------------------------  |
| a     | gtfs:CalendarRule |
| gtfs:monday     | $(monday) |
| gtfs:tuesday     | $(tuesday) |
| gtfs:wednesday     | $(wednesday) |
| gtfs:thursday     | $(thursday) |
| gtfs:friday     | $(friday) |
| gtfs:saturday     | $(saturday) |
| gtfs:sunday     | $(sunday) |
| schema:startDate     | $(start_date) |
| schema:endDate     | $(end_date) |




## feed
| Property       |                Collation.                   |
| :----------- | :----------------------------------  |
| a     | gtfs:Feed |
| dct:publisher     | $(feed_publisher_name) |
| foaf:page     | $(feed_publisher_url)~iri |
| dct:language     | $(feed_lang) |
| schema:startDate     | $(feed_start_date) |
| schema:endDate     | $(feed_end_date) |
| schema:version     | $(feed_version) |




## shapes
| Property       |                Collation.                   |
| :----------- | :----------------------------------  |
| a     | gtfs:Shape |
| p     | o |




## shapePoints
| Property       |                Collation.                   |
| :----------- | :----------------------------------  |
| a     | gtfs:ShapePoint |
| geo:lat     | $(shape_pt_lat) |
| geo:long     | $(shape_pt_lon) |
| gtfs:pointSequence     | $(shape_pt_sequence) |
| gtfs:distanceTraveled     | $(shape_dist_traveled) |




## frequencies
| Property       |                Collation.                   |
| :----------- | :----------------------------------  |
| a     | gtfs:Frequency |
| gtfs:startTime     | $(start_time) |
| gtfs:endTime     | $(end_time) |
| gtfs:headwaySeconds     | $(headway_secs) |
| gtfs:exactTimes     | $(exact_times) |
| p     | o |

