
{% for j in join_list +%}
- **Join Condition**:
    - Source triples map: **{{ subject }}**
    - Target triples map: **{{ j['parentTriplesMap'] }}**
    - Function: **equal({{ j['child'] }}, {{ j['parent'] }})**

```mermaid
%%{ init : { "theme" : "base", "flowchart" : { "curve" : "linear" }}}%%

flowchart LR
S{{ loop.index }}["{{ j['subject'] }}"] -->|"{{ j['predicate'] }}"| object{{ loop.index }}("{{ j['template'] }}")

``` 

{%+ endfor +%} 