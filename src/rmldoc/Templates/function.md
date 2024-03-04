- **joinCondition**: is used to specify the conditions under which two data sources or tables should be joined when creating RDF triples through mappings.
{% for j in join_list %}
Function: **equal({{ j['child'] }}, {{ j['parent'] }})** conditions for joining.
 
```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S{{ loop.index }}["{{ j['subject'] }}"] -->|"{{ j['predicate'] }}"| object{{ loop.index }}("{{ j['template'] }}")

``` 

{%+ endfor %} 