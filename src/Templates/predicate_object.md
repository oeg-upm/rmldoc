- **Predicate Object**

| Property       | Column |
| :----------- |:-------|
{% for po in pom -%}
| {{ po['predicate'] }} | {{ po['object'] }} |
{%+ endfor %}