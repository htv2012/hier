"""
Prints hierarchical data.

This data can be JSON, TOML, XML, YAML, or even a file system's directory.

- If the path is a directory, prints its content like that of the tree command
- If the path points to a JSON, TOML, XML, or YAML file, prints its content
"""

import argparse
import importlib.metadata
import json
import pathlib
import tomllib
import xml.etree.ElementTree as ET

import yaml

from . import print_hier

CLI_NAME = "hier"

try:
    __version__ = importlib.metadata.version(CLI_NAME)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"


def main():
    parser = argparse.ArgumentParser(
        prog=CLI_NAME,
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path")
    parser.add_argument(
        "-V", "--version", action="version", version=f"{CLI_NAME} v{__version__}"
    )
    options = parser.parse_args()

    path = pathlib.Path(options.path)
    if path.is_dir():
        print_hier(path)
        return

    parsers = {
        ".json": json.load,
        ".toml": tomllib.load,
        ".xml": ET.parse,
        ".yaml": yaml.safe_load,
        ".yml": yaml.safe_load,
    }
    parse = parsers.get(path.suffix)
    if parse is None:
        raise SystemExit(f"File type not supported: {path}")

    with open(options.path, "rb") as stream:
        data = parse(stream)
    print_hier(data)


if __name__ == "__main__":
    main()
