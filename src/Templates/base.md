# RML Documentation (RMLdoc)

**Version:**
{% block version %}{% endblock %}
**Authors**: 
{%- block authors %}{% endblock %}
**Mapping file:**
{%- block mapping_file %}{% endblock %}
**License**:

[![http://insertlicenseURIhere.org](https://img.shields.io/badge/License-Creative%20Commons%20Attribution%204.0%20International%20(CC%20BY%204.0)-blue.svg)](https://creativecommons.org/licenses/by/4.0/)

------


## **Namespaces used in the document**
{% block prefixes %}{% endblock %}

## Mappings
>[!NOTE]
>1. **Source**: This is where you define the source of your data, which can be a relational database, a CSV file, or any other structured data source. The logical source specifies the location and format of your source data.
>2. **Subject**: This part of the mapping defines how the data from the logical source will be used to create RDF subjects, typically using templates and column mappings.
>3. **Predicate Object**: These describe how the data from the logical source will be used to generate RDF triples, indicating relationships between subjects and objects.
>4. **joinCondition**:is used to specify the conditions under which two data sources or tables should be joined when creating RDF triples through mappings.
{% block mapping %}{% endblock %}


----
{% block copyright %}
**Copyright © 2024** *[Ontology Engineering Group](https://oeg.fi.upm.es/)*, *[Universidad Politécnica de Madrid](https://www.upm.es/internacional)*.
{% endblock %}