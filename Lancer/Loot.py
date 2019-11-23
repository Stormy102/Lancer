import json

loot = {}


def to_json():
    output = json.dumps(loot, sort_keys=True, indent=4)
    print(output)