- **joinCondition**: This is used for specifying conditions for joining different data sources or tables.
In this representation, **equal**() specifies the conditions for joining. The **<#TriplesMap1>**.field1 and **<#TriplesMap2**>.field2 represent the values field1, fiel2 in the TM1 and TM2 used for the join.
```mermaid
%%{ init : { "theme" : "forest", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
{% for j in join_list -%}
S["{{ j['subject'] }}"] .- B{{ loop.index }}
subgraph s{{ loop.index }}["equal({{ subject}}.{{ j['child'] }}, {{ j['parentTriplesMap']}}.{{ j['parent'] }})"]
B{{ loop.index }}("{{ j['predicate'] }}")
end
B{{ loop.index }} .-> o{{ loop.index }}("{{ j['template'] }}")
{%+ endfor %}  
``` 

