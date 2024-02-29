import logging
from jinja2 import Environment, FileSystemLoader


class rmldoc:
    def __init__(self):
        self.log = logging.getLogger("RML Mapping Documentation(rmldoc)")

    def rmd_header(self, namespaces):
        environment = Environment(loader=FileSystemLoader("templates/"))
        template = environment.get_template("rmd.md")

    def rmd_version(self):
        return ""

    def rmd_authors(self):
        return ""

    def rmd_license(self):
        return ""

    def rmd_prefixes(self):
        return ""

    def rmd_mappings(self):
        return ""
