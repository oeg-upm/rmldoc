[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) 
[![License](https://camo.githubusercontent.com/db9dfde8049c5d66ba62fde707d2cfb30e26f9f26ff274c3442c0aec1ec410a4/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d417061636865253230322e302d626c75652e737667)](https://github.com/oeg-upm/rmldoc/blob/main/LICENSE) 
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10731583.svg)](https://doi.org/10.5281/zenodo.10731583)
 [![Latest PyPI version](https://img.shields.io/pypi/v/rmldoc?style=flat)](https://pypi.python.org/pypi/rmldoc)

# RMLdoc

RMLdoc is a tool designed to simplify the process of generating documentation of mappings used for knowledge graph construction. It automates the documentation generation process, allowing users to easily understand the mapping transformation rules defined within their projects. Given an input mapping file written in R2RML, RML, or YARRRML, RMLdoc will generate a detailed Markdown documentation explaining each mapping with corresponding diagrams, in a human readable manner.

## Features

- **Automated Documentation Generation**: RMLdoc automatically generates documentation for mappings, eliminating the need for manual documentation efforts.
- **Clear and Readable Output**: The generated documentation provides clear and concise descriptions of the input data sources, subject and predicate-object descriptions, along with other components defined within the mappings and their metadata.
- **Command-Line Interface (CLI)**: RMLdoc provides a simple command-line interface for easy integration into existing workflows and build processes.

## Installation

### From pypi
RMLdoc is available in pypi!

```bash
pip install rmldoc
```

### From source

To install RMLdoc, simply clone this repository and cd in the main folder. Then install the package:

```
pip install -e .
```
## Usage

**rmldoc** offers the following options:

```bash
usage: rmldoc [-h] -i INPUT_MAPPING_PATH [-o OUTPUT_PATH]

optional arguments:
  -h, --help            show this help message and exit
  
  -i INPUT_MAPPING_PATH, --input_mapping_path INPUT_MAPPING_PATH
                        Path to the input mapping file in RML format.
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Path to save the generated document. Default output in output.md
  -y, --yatter          Enable yatter option to read yarrrml mappings

```


To generate documentation for your mappings, use the following command, where you would replace `path/to/rml/mappings.rml` with the path to your RML mapping file and `path/to/output/directory/mappings.md` with the file where you want the documentation to be generated:

```bash
rmldoc -i path/to/rml/mappings.rml - o path/to/output/directory/mappings.md
```

To automate documentation generation using GNU's [make](https://www.gnu.org/software/make/manual/make.html), a typical implementation would involve creating a *makefile* with the following structure:
```makefile
doc-rml:  ## Generate documentation for RML
	@echo -e "\033[35m > Generate documentation for RML \033[0m - requires RMLdoc: see https://github.com/oeg-upm/rmldoc"
	@find mapping/ -type f -name *.ttl \
		-printf "\n%f\n" \
		-exec rmldoc -i {} -o {}.md \;
	@echo -e "\033[35m > Done  \033[0m"
```

## Example

The following [link](https://github.com/oeg-upm/rmldoc/blob/main/example/example.md) shows the result produced by `RMLdoc` from the following [mapping file](https://github.com/oeg-upm/rmldoc/blob/main/example/example_input.ttl).

## RMLdoc specification

The [RMLdoc specification](https://github.com/oeg-upm/rmldoc/blob/main/spec/specification.md) describes the main metadata expected in a RML mapping file. Have a look to create eye-catching documentations!

## Contributing

Contributions to `RMLdoc` are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## Authors

* [Jhon Toledo](https://github.com/jatoledo) ([ja.toledo@upm.es](mailto:ja.toledo@upm.es))
* [Ana Iglesias-Molina](https://github.com/anaigmo)
* [David Chaves-Fraga](https://github.com/dachafra)
* [Daniel Garijo](https://github.com/dgarijo)
