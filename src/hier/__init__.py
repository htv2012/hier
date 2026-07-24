import functools
import pathlib
import xml.etree.ElementTree as ET
from typing import Optional, TextIO


@functools.singledispatch
def print_hier(data, prefix: str = "", file: Optional[TextIO] = None):
    raise NotImplementedError(f"Not implemented for type {type(data)}: {data}")


@print_hier.register
def _(data: list, prefix: str = "", file: Optional[TextIO] = None):
    count = len(data)

    for i, entry in enumerate(data):
        is_last = i == count - 1
        connector = "└── " if is_last else "├── "

        if isinstance(entry, (list, dict)):
            print(f"{prefix}{connector}[{i}]", file=file)
            extension = "    " if is_last else "│   "
            print_hier(entry, prefix + extension)
        else:
            print(f"{prefix}{connector}[{i}]={entry!r}", file=file)


@print_hier.register
def _(data: dict, prefix: str = "", file: Optional[TextIO] = None):
    count = len(data)

    for i, (key, value) in enumerate(data.items()):
        is_last = i == count - 1
        connector = "└── " if is_last else "├── "

        if isinstance(value, (list, dict)):
            print(f"{prefix}{connector}{key}", file=file)
            extension = "    " if is_last else "│   "
            print_hier(value, prefix + extension)
        else:
            print(f"{prefix}{connector}{key}={value!r}", file=file)


def format_node(node: ET.Element, file: Optional[TextIO] = None):
    text = (node.text or "").strip()
    attributes = ", ".join(f"{k}={v!r}" for k, v in node.items())
    if attributes:
        attributes = f"  # {attributes}"

    if text:
        out = f"{node.tag}={text!r}{attributes}"
    else:
        out = f"{node.tag}{attributes}"
    return out


@print_hier.register
def _(data: ET.ElementTree, prefix: str = "", file: Optional[TextIO] = None):
    root = data.getroot()
    assert root is not None
    print(f"{prefix}{format_node(root)}", file=file)
    print_hier(root)


@print_hier.register
def _(data: ET.Element, prefix: str = "", file: Optional[TextIO] = None):
    nodes = list(data)
    count = len(nodes)

    for i, node in enumerate(nodes):
        is_last = i == count - 1
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "
        print(f"{prefix}{connector}{format_node(node)}", file=file)
        print_hier(node, prefix + extension)


@print_hier.register
def _(data: pathlib.Path, prefix: str = "", file: Optional[TextIO] = None):
    entries = sorted(data.iterdir(), key=lambda p: p.name)
    count = len(entries)

    for i, entry in enumerate(entries):
        is_last = i == count - 1
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{entry.name}", file=file)

        if entry.is_dir():
            extension = "    " if is_last else "│   "
            print_hier(entry, prefix + extension)
