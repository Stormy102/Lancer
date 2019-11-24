import json

loot = {}


def to_json():
    return json.dumps(loot, sort_keys=True, indent=4)