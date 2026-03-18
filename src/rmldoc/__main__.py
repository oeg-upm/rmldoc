__author__ = "Jhon Toledo"
__credits__ = ["Jhon Toledo"]
__copyright__ = "Copyright © 2024 Jhon Toledo"
__license__ = "Apache-2.0"
__maintainer__ = "Jhon Toledo"
__email__ = "ja.toledo@upm.es"

import argparse
import os
import logging
from rmldoc.workflows import workflow_md, workflow_html
from pathlib import Path

def setup_logging():
    logger = logging.getLogger("rmd_main")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger


log = setup_logging()


def define_args():
    """Define command-line arguments for the script."""
    parser = argparse.ArgumentParser(description="Generate documentation from RML/YARRRML mappings.")
    parser.add_argument(
        "-i", "--input_mapping_path", required=True,
        help="Path to the input mapping file in RML format."
    )
    parser.add_argument(
        "-o", "--output_path", default="output.md",
        help="Path to save the generated document (default: output.md)."
    )
    parser.add_argument(
        "-y", "--yatter", action='store_true',
        help="Enable YARRRML support to read mappings in YARRRML format."
    )
    parser.add_argument(
        "-f", "--format", choices=["md", "html"], default="md",
        help="Specify output format: 'md' for Markdown or 'html' for HTML (default: 'md')."
    )
    return parser


def main():
    """Main function to execute the script."""
    args = define_args().parse_args()

    log.info("Starting RML Documentation generation.")
    log.info(f"Input Mapping Path: {args.input_mapping_path}")
    log.info(f"Output Format: {args.format}")

    output_path = args.output_path
    if args.format == "html" and not output_path.endswith(".html"):
        output_path = os.path.splitext(output_path)[0] + ".html"
    elif args.format == "md" and not output_path.endswith(".md"):
        output_path = os.path.splitext(output_path)[0] + ".md"

    try:
        if args.format == "html":

            workflow_html(Path(args.input_mapping_path), output_path)

        else:
            workflow_md(args.input_mapping_path, output_path)
    except Exception as e:
        log.error("An error occurred during the workflow execution.", exc_info=e)


if __name__ == "__main__":
    main()
