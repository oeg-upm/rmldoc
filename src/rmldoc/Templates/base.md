{% block title %}{% endblock -%}
**Version:**
{% block version %}{% endblock %}
**Authors**: 
{%- block authors %}{% endblock %}
**Mapping file:**
{%- block mapping_file %}{% endblock %}
{%- block description %}{% endblock %}
{%- block dateCreated %}{% endblock %}
**License**:
{%- block license %}{% endblock %}

------


## **Namespaces used in the document**
{% block prefixes %}{% endblock %}

## Mappings
>[!NOTE]
>1. **Source**: This is where you define the source of your data, which can be a relational database, a CSV file, or any other structured data source. The logical source specifies the location and format of your source data.
>2. **Subject**: This part of the mapping defines how the data from the logical source will be used to create RDF subjects, typically using templates and column mappings.
>3. **Predicate Object**: These describe how the data from the logical source will be used to generate RDF triples, indicating relationships between subjects and objects.
>4. **JoinCondition**: is used to specify the conditions under which two data sources or tables should be joined when creating RDF triples through mappings.

{% block mapping %}{% endblock %}


----
{% block copyright %}
**This documentation was generated using**  *[RMLdoc](https://oeg-upm.github.io/rmldoc/)*.
{% endblock %}