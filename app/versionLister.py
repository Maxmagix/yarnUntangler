import requests
import time
import json


def getCurrentVersion(data, name):
    if ('resolved' not in data[name].keys()):
        return ''
    url = data[name]['resolved'].split('/-/')[0]
    resp = requests.get(url)
    package_data = json.loads(resp.content)
    if ('dist-tags' in package_data.keys()):
        return package_data['dist-tags']['latest']
    return ''


def versionnedPackages(data, requirements):
    # dependencies->names->version

    # get all versions by level for each package
    aggregated_names = {}
    for level in requirements.keys():
        for req in requirements[level].keys():
            if (req not in aggregated_names):
                aggregated_names[req] = {}
            aggregated_names[req][level] = requirements[level][req]
    unique_filtered_requirements = aggregated_names.keys()
    # names->dependencies->version

    # we find all matching packages in data (listing installed versions)
    matching_packages = {}
    for requirement in unique_filtered_requirements:
        for level in aggregated_names[requirement]:
            if (requirement not in matching_packages.keys()):
                matching_packages[requirement] = []
            # double set to ensure no double in final array and to use filter as array
            matching_packages[requirement] += list(set(filter(lambda x: f"{requirement}@{aggregated_names[requirement][level]}" in x, data.keys())))
        matching_packages[requirement] = list(set(matching_packages[requirement]))
    # react-dom -> [react-dom@1, react-dom@2]
    packages = {}
    # ex react-dom
    for package in matching_packages.keys():
        print(package)
        latest = getCurrentVersion(data, matching_packages[package][0])  # should be the same resolver for all
        time.sleep(0.1)
        for one_version in matching_packages[package]:  # loop on react-dom@1, react-dom@2
            at_level = [] # list all levels in which this version is found
            for level in aggregated_names[package]:
                if (f"{package}@{aggregated_names[package][level]}" in one_version):
                    at_level.append(level)
            for level in at_level:
                if (package in packages.keys()):
                    packages[package]['version'][level] = data[one_version]['version']
                else:
                    packages[package] = {'version': {}, 'latest': latest, 'target': aggregated_names[package]}
                    packages[package]['version'][level] = data[one_version]['version']

    return packages


# Make an excel file for each dependency object with it's packages (target version, current version, latest version)
def saveExcel_versions(listRequirements, listName, packages):
    import pandas as pd
    table = {}
    list_requirements = listRequirements.keys()

    def filterByKey(pair):
        key, value = pair
        return key in list_requirements

    packages_needed = dict(filter(filterByKey, packages.items()))
    attrs = ['version', 'latest', 'target']
    table['package'] = packages_needed.keys()
    for attr in attrs:
        def stepInLevelOptional(item):
            if (type(item[attr]) is dict and len(item[attr].keys())):
                return item[attr]['level']
            return item[attr]
        table[attr] = list(map(stepInLevelOptional, packages_needed.values()))
    print('version', len(table['version']))
    print('latest', len(table['latest']))
    print('package', len(table['package']))

    df = pd.DataFrame(table)
    df.to_excel(f"./{listName}.xlsx")
