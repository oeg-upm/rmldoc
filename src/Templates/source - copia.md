- **Source**

| Feature | Value         | label                 | comment                 |
| ------- |---------------|-----------------------|-------------------------|
{% for s in source -%}
| {{ "Source" }}     | {{ s['source'] }} | {{ s['label'] }} | {{ s['comment'] }} |
{%+ endfor %}