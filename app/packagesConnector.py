from .utilsVersion import splitVersion, mergeVersion


# a first version, grouping packages by name
def group_packages(data):
    raw_packages = list(data.keys())
    packages = {}
    connections = []
    for package in raw_packages:
        names = package.split(',')
        [name, version] = splitVersion(names[0])
        # one instance per package (multiple targets)
        if (name in packages.keys()):
            packages[name]['target'] = makeArray(packages[name]['target'])
            packages[name]['target'].append(version)
        else:
            packages[name] = {'target': version}

        # if multiple versions in package name (comma)
        if (len(names) > 1):
            packages[name]['target'] = makeArray(packages[name]['target'])
            for other_name in names:
                [n, other_version] = splitVersion(other_name)
                if (other_version not in packages[name]['target']):
                    packages[name]['target'].append(other_version)

        # make connections between package@version and dependency@version
        if ('dependencies' in data[package].keys()):
            for dep in data[package]['dependencies'].keys():
                connections_origins = map(lambda x: x[0], connections)
                connections_targets = map(lambda x: x[1], connections)
                full_dep = mergeVersion(dep, data[package])

                if not (package in connections_origins and
                        full_dep in connections_targets):
                    connections.append((package, full_dep))
        # fill attributes for package view
        attributes = ['version', 'dependencies']
        for attribute in attributes:
            if (attribute in data[package].keys()):
                packages[name][attribute] = data[package][attribute]
    return packages, connections


# a second version, making an index for each package/target version
def detailledConnectPackages(data):
    raw_packages = list(data.keys())
    packages = {}
    connections = []
    for package in raw_packages:
        names = map(lambda x: x.strip(), package.split(','))
        for name in names:
            packages[name] = {'isRoot': False,  'original_name': package}
            if ('dependencies' in data[package].keys()):
                for dep in data[package]['dependencies'].keys():
                    connections_origins = map(lambda x: x[0], connections)
                    connections_targets = map(lambda x: x[1], connections)
                    full_dep = mergeVersion(dep, data[package])

                    if not (name in connections_origins and
                            full_dep in connections_targets):
                        connections.append((name, full_dep))
            # fill attributes for package view
            attributes = ['version', 'dependencies']
            for attribute in attributes:
                if (attribute in data[package].keys()):
                    packages[name][attribute] = data[package][attribute]
    return packages, connections
