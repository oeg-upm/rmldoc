- **joinCondition**: This is used for specifying conditions for joining different data sources or tables.
```mermaid
%%{ init : { "theme" : "forest", "flowchart" : { "curve" : "stepBefore" }}}%%
classDiagram
direction LR
{% for j in join_list -%}
{{ subject }} --> {{ j['parentTriplesMap'] }} : {{ j['predicate'] }}
{{ subject }}: {{ j['child'] }}
{{ subject }}: equal({{ j['child'] }}, {{ j['parent'] }})
{{ j['parentTriplesMap'] }}: {{ j['parent'] }}
<<TriplesMap>> {{ subject }} 
<<TriplesMap>> {{ j['parentTriplesMap'] }}
{%+ endfor %}   
``` 

