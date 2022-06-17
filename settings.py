import json

def load_json(filename):
    with open(filename+'.json', 'r') as json_file:
        obj = json.load(json_file)
    return obj
