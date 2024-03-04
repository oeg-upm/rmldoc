- **joinCondition**:
{% for j in join_list %}
Function: **equal({{ j['child'] }}, {{ j['parent'] }})** conditions for joining.
 
```mermaid
%%{ init : { "theme" : "forest", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S{{ loop.index }}["{{ j['subject'] }}"] -->|"{{ j['predicate'] }}"| object{{ loop.index }}("{{ j['template'] }}")

``` 

{%+ endfor %} 