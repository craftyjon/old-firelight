"""FireLight utilities"""
import pickle


def serialize(thing):
    return pickle.dumps(thing, protocol=pickle.HIGHEST_PROTOCOL)


def deserialize(string):
    return pickle.loads(string)
