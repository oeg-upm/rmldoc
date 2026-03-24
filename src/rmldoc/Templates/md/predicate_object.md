- **Predicate Object**

| Predicate | Object |
|:----------|:-------|
{% for po in pom -%}
| {{ po['predicate'] }} | {{ po['object'] }} |
{%+ endfor %}