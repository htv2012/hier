import contextlib
import functools
import pathlib
import xml.etree.ElementTree as ET
from typing import Optional, TextIO


def element_tree_iterator(data):
    root = data.getroot()
    return list(root)


def get_iterator(data):
    if isinstance(data, list):
        return list
    elif isinstance(data, dict):
        return dict.items
    elif isinstance(data, pathlib.Path):
        return pathlib.Path.iterdir
    elif isinstance(data, ET.Element):
        return list
    elif isinstance(data, ET.ElementTree):
        return element_tree_iterator
    raise TypeError(f"cannot handle data type {data.__class__.__name__}")


def fmt_root(data):
    if isinstance(data, pathlib.Path):
        return str(data)
    elif isinstance(data, ET.ElementTree):
        root = data.getroot()
        return root.tag
    return ""


def get_child(entry):
    if isinstance(entry, tuple):
        return entry[1]  # dict
    return entry


def is_container(entry) -> bool:
    if isinstance(entry, ET.Element):
        return list(entry) != []
    elif isinstance(entry, (list, dict)):
        return True
    elif isinstance(entry, pathlib.Path):
        with contextlib.suppress(NotADirectoryError):
            return list(entry.iterdir()) != []
        return False
    return False


def fmt_node(index, entry) -> str:
    if isinstance(entry, tuple) and len(entry) == 2:
        return f"{entry[0]}={entry[1]!r}"
    elif isinstance(entry, ET.Element):
        value = entry.text.strip()
        value = f"={value!r}" if value else ""
        return f"{entry.tag}{value}"
    elif isinstance(entry, pathlib.Path):
        return entry.name

    # must be a list entry if gets this far
    child = get_child(entry)
    if is_container(child):
        return f"[{index}]"
    else:
        return f"[{index}]={entry}"


def hier(data, prefix: str = "", file: Optional[TextIO] = None):
    # print just the root and let _hier handle the children
    root = fmt_root(data)
    if root:
        print(f"{prefix}{root}", file=file)
    _hier(data, prefix, file)


def _hier(data, prefix: str = "", file: Optional[TextIO] = None):
    iterator = get_iterator(data)
    children = list(iterator(data))
    count = len(children)

    for i, entry in enumerate(children):
        is_last = i == count - 1
        connector = "└── " if is_last else "├── "

        child = get_child(entry)
        formatted_node = fmt_node(i, entry)
        print(f"{prefix}{connector}{formatted_node}", file=file)
        if is_container(child):
            extension = "    " if is_last else "│   "
            _hier(child, prefix + extension)


# ======================================================================
# Old code, to be removed
# ======================================================================


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
