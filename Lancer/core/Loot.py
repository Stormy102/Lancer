import json

loot = {}


def reset():
    loot = {}


def to_json():
    return json.dumps(loot, sort_keys=True, indent=4)