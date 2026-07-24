import contextlib
import pathlib
import xml.etree.ElementTree as ET
from typing import Optional, TextIO


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
        return lambda d: list(d.getroot())
    raise TypeError(f"cannot handle data type {data.__class__.__name__} {data=}")


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


def fmt_root(data):
    if isinstance(data, pathlib.Path):
        return str(data)
    elif isinstance(data, ET.ElementTree):
        root = data.getroot()
        return root.tag
    return ""


def fmt_node(index, entry, container: bool) -> str:
    if isinstance(entry, tuple) and len(entry) == 2:
        name, value = entry
        if container:
            return str(name)
        return f"{name}={value!r}"
    elif isinstance(entry, ET.Element):
        text = (entry.text or "").strip()
        attributes = ", ".join(f"{k}={v!r}" for k, v in entry.items())
        if attributes:
            attributes = f"  # {attributes}"

        if text:
            out = f"{entry.tag}={text!r}{attributes}"
        else:
            out = f"{entry.tag}{attributes}"
        return out
    elif isinstance(entry, pathlib.Path):
        return entry.name

    # must be a list entry if gets this far
    if container:
        return f"[{index}]"
    else:
        return f"[{index}]={entry}"


def print_hier(data, prefix: str = "", file: Optional[TextIO] = None):
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
        container = is_container(child)
        formatted_node = fmt_node(i, entry, container)
        print(f"{prefix}{connector}{formatted_node}", file=file)
        if container:
            extension = "    " if is_last else "│   "
            _hier(child, prefix + extension)
