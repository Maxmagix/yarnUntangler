from .utilsVersion import splitVersion, mergeVersion

# use a separate variable that has the roots
def aglomerateAnyRootWithDetail(packages):
    aglomeratedPackages = {}

    for package in packages:
        names = package.split(',')
        [namePackage, version] = splitVersion(names[0])
        aglomeratedPackages[namePackage] = {}

        def stepRoot(packages, name, depth, leafcrumb):
            allnames = package.split(',')
            versions = map(lambda x: splitVersion(x)[1], allnames)
            [shortName, version] = splitVersion(allnames[0])

            # prevent infinite loops by keeping track of visited branches
            if (depth < 400 and 'dependencies' in packages[name].keys() and name not in leafcrumb):
                leafcrumb.append(name)
                for dep in packages[name]['dependencies'].keys():
                    if (dep not in aglomeratedPackages.keys()):
                        aglomeratedPackages[dep] = {}
                    full_dep = mergeVersion(dep, packages[name])
                    if ('roots' not in aglomeratedPackages[dep].keys()):
                        aglomeratedPackages[dep]['roots'] = {}
                    if (shortName not in aglomeratedPackages[dep]['roots']):
                        aglomeratedPackages[dep]['roots'][shortName] = []
                    aglomeratedPackages[dep]['roots'][shortName] += versions
                    packages = stepRoot(packages, full_dep, depth + 1, leafcrumb)
            return packages
        packages = stepRoot(packages, package, 0, [])
    return aglomeratedPackages


# add roots to the packages recursively
def addRootsOnBranches(packages, name, depth, leafcrumb):
    # prevent infinite loops by keeping track of visited branches
    if (depth < 400 and 'dependencies' in packages[name].keys() and name not in leafcrumb):
        leafcrumb.append(name)
        for dep in packages[name]['dependencies'].keys():
            full_dep = mergeVersion(dep, packages[name])
            if ('roots' not in packages[full_dep].keys()):
                packages[full_dep]['roots'] = []
            if (name not in packages[full_dep]['roots']):
                packages[full_dep]['roots'].append(name)
                packages[full_dep]['roots'].sort()
            packages = addRootsOnBranches(packages, full_dep, depth + 1, leafcrumb)
    return packages


def buildTree(packages):
    final_tree = []
    for package in packages:
        if (packages[package]['isRoot'] and packages[package]['original_name'] not in final_tree):
            final_tree.append(packages[package]['original_name'])
    return final_tree
