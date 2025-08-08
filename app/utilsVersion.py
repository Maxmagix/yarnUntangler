def mergeVersion(str, data):
    return str + '@' + data['dependencies'][str]


def splitVersion(str):
    return str.rsplit('@', 1)


def makeArray(value):
    if (type(value).__name__ != "list"):
        return [value]
    return value
