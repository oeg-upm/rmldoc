```diff
- RED text
+ GREEN text
! ORANGE text
# GRAY text
```

 
# Prefixes
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
| Property       |                Collation.                   |
| :----------- | :----------------------------------  |
| a     | gtfs:StopTime |
| gtfs:arrivalTime     | $(arrival_time) |
| gtfs:departureTime     | $(departure_time) |
| gtfs:stopSequence     | $(stop_sequence) |
| gtfs:headsign     | $(stop_headsign) |
| gtfs:pickupType     | http://transport.linkeddata.es/resource/PickupType/$(pickup_type)~iri |
| gtfs:dropOffType     | http://transport.linkeddata.es/resource/DropOffType/$(drop_off_type)~iri |
| gtfs:distanceTraveled     | $(shape_dist_traveled) |
| p     | o |
| p     | o |




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
| gtfs:shortName     | $(route_short_name) |
| gtfs:longName     | $(route_long_name) |
| dct:description     | $(route_desc) |
| gtfs:routeType     | http://transport.linkeddata.es/resource/RouteType/$(route_type)~iri |
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

