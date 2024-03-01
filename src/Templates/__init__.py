import logging


class Templates:
    def __init__(self):
        self.log = logging.getLogger("Templates")
        self.log.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))

        self.log.handlers.clear()
        self.log.addHandler(ch)

    def mapping_prefixes(self):
        prefix_template = """
# Prefixes
| Prefix       |               IRI.                   |
| :----------- | :----------------------------------  |
{% for key, value in my_mapping.prefixes.items() -%}
| {{ key }}     | {{ value }} |
{%+ endfor %}
        """
        return prefix_template

    def mappings(self):
        mapping_template = """
# mappings
The mappings collection
{% for key, value in my_mapping.mappings.items() %}
{#   Key: {{ key }}, Value: {{ value }} #}  



## {{ key }}
### Source
| Feature | Value                    |
| ------- | ------------------------ |
{% for i in value.sources -%}
| sources | {{ i }} |   
{%+ endfor %}


### Subject
| URI                                                          |
| ------------------------------------------------------------ |
| {{ value.s }} |

### Predicate object    
| Property       |                Collation.                   |                DataType                |
| :----------- | :----------------------------------  | -----------------------------------  |
{% for predicate_obj in value.po -%}
| {{ predicate_obj[0] }}    | {{ predicate_obj[1] }} |  {{ predicate_obj[2] }} |
{%+ endfor %}
{% endfor %}

        """
        return mapping_template

# {# {% if predicate_obj  is mapping %}
#     | {{ predicate_obj.p }}    |
# {{ predicate_obj }}
# {% endif %} #}