
def makeJaalGraph(packages, connections):
    import pandas as pd
    from jaal import Jaal

    edges_raw = {}
    edges_raw['from'] = map(lambda x: x[0], connections)
    edges_raw['to'] = map(lambda x: x[1], connections)

    nodes_raw = {}
    first_package = list(packages.keys())[0]
    for attribute in packages[first_package].keys():
        def fillAttribute(x):
            if (attribute in x.keys()):
                return x[attribute]
            return None
        nodes_raw[attribute] = map(fillAttribute, packages.values())
    nodes_raw['id'] = list(packages.keys())
    Jaal(pd.DataFrame(edges_raw), pd.DataFrame(nodes_raw)).plot(directed=True)
