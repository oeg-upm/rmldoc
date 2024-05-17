# RMLdoc demo

RMLdoc is a tool designed to simplify the process of generating documentation of mappings used for knowledge graph construction. It automates the documentation generation process, allowing users to easily understand the mapping transformation rules defined within their projects. Given an input mapping file written in R2RML, RML, or YARRRML, RMLdoc will generate a detailed Markdown documentation explaining each mapping with corresponding diagrams, in a human readable manner.

## Table of Contents


- [Installation](#installation)
- [Usage](#usage)
- [RMLdoc Metadata](#rmldoc-metadata)
- [Contact](#contact)



## Installation

```commandline
# Clone the repository
git clone https://github.com/oeg-upm/rmldoc.git

# Change to the project directory
cd rmldoc

# Install the package
pip install -e .
```
## Usage

```commandline
usage: rmldoc [-h] -i INPUT_MAPPING_PATH [-o OUTPUT_PATH]

optional arguments:
  -h, --help            show this help message and exit
  
  -i INPUT_MAPPING_PATH, --input_mapping_path INPUT_MAPPING_PATH
                        Path to the input mapping file in RML format.
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Path to save the generated document. Default output in output.md
  -y, --yatter          Enable yatter option to read yarrrml mappings

```
## RMLdoc Metadata

### Contributors
```commandline
map:person_000 dct:contributor foaf:Person ;
	rdfs:label "Jhon Toledo" ;
	foaf:mbox <mailto:ja.toledo@upm.es> .

map:person_001 dct:contributor foaf:Person ;
	rdfs:label "Ana Iglesias-Molina" .

```
### Dataset

```commandline
    map:rules_000 schema:contributor map:person_000, map:person_001 ;
	<http://rdfs.org/ns/void#exampleResource> map:map_stoptimes_000 ;
	rdf:type schema:Dataset;
    schema:version "0.1.0";
    schema:title "GTFS-Madrid-Bench CSV mapping";
    schema:dateCreated "03-05-2024";
    schema:description "This is a mapping definition written in the RML syntax, which is used to map CSV data into RDF (Resource Description Framework) format.".

```
### Contact
https://github.com/oeg-upm/rmldoc