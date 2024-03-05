{% extends "base.md" %}
{% block title -%}
{% for v in version %}
   {% if v['title']!='None' %}
# {{ v['title']}}
   {% else %}
# Mapping Documentation
   {% endif %}
{%- endfor %}
{% endblock %}
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
{%- block license %}
{% for v in version -%}
{% if 'https://creativecommons.org/licenses/by/4.0' in v['license'] or v['license']=='None' %}
[![http://insertlicenseURIhere.org](https://img.shields.io/badge/License-Creative%20Commons%20Attribution%204.0%20International%20(CC%20BY%204.0)-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
{% else %}
{{ v['license'] }}
{% endif %}
{%- endfor -%}
{% endblock %}
{%- block description %}
{% for v in version -%}
{% if v['description']!='None' %}
**Description**: {{ v['description'] }}
{% endif %}
{%- endfor -%}
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