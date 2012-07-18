"""FireLight utilities"""
import json


def serialize(thing):
    return json.dumps(thing)


def deserialize(string):
    return json.loads(string)
