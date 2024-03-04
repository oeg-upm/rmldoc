{% extends "base.md" %}
{% block version -%}
{% for v in version -%}
   {% if v['version']!='' %}
* {{ v['version']}}
   {% endif %}
{%- endfor %}
{%- endblock %}
{# -- block authors--#}
{% block authors %}
{% for author in authors -%}
    {% if author['author']!='' %}
* {{ author['author']}}
   {% endif %}
{%- endfor %}
{% endblock %}
{% block mapping_file %}
{{ mapping_file }}
{% endblock %}
{# -- block prefixes-- #}
{% block prefixes %}
| Prefix       |               IRI.                   |
| :----------- | :----------------------------------  |
{% for prefix in prefixes -%}
| {{ prefix[0] }}     | {{ prefix[1] }} |
{%+ endfor %}
{% endblock %}
{# -- block Mappings-- #}
{% block mapping %}
{{ mapping_content }}
{% endblock %}