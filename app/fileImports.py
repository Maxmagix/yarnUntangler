from pyarn import lockfile
import json


def openFile():
    pathfile = "./yarn.lock"
    my_lockfile = lockfile.Lockfile.from_file(pathfile)
    return my_lockfile.data


def loadRequirements():
    pathfile = './packages.json'
    with open(pathfile, 'r') as f:
        jsonfile = json.load(f)
    accepted_keys = ["dependencies", "devDependencies", "peerDependencies"]

    def filterKeys(pair):
        key, value = pair
        return key in accepted_keys
    return dict(filter(filterKeys, jsonfile.items()))
