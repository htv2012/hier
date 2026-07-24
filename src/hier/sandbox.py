import pathlib
import xml.etree.ElementTree as ET

from hier import hier


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


objects = [
    dict(ab=1, cd=2, ef=3),
    ["peter", "paul", "mary", ["one", "two"]],
    pathlib.Path("src/hier"),
    ET.parse("samples/kens_books.xml"),
]

for obj in objects:
    print()
    print("# =========================================================================")
    print(f"# {obj.__class__.__name__}")
    print("# =========================================================================")
    hier(obj)
