import pathlib
import xml.etree.ElementTree as ET


def get_iterator(data):
    if isinstance(data, list):
        return list
    elif isinstance(data, dict):
        return dict.items
    elif isinstance(data, pathlib.Path):
        return pathlib.Path.iterdir
    elif isinstance(data, ET.Element):
        return list


objects = [
    dict(ab=1, cd=2, ef=3),
    ["peter", "paul", "mary"],
    pathlib.Path("src/hier"),
    ET.fromstring("<details><uid>501</uid><alias>Anna</alias></details>"),
]

for obj in objects:
    iterator = get_iterator(obj)
    for entry in iterator(obj):
        print(entry)
    print("=" * 80)
