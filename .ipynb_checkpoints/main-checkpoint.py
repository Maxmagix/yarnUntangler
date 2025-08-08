from app.fileImports import openFile, loadRequirements
from app.packagesConnector import detailledConnectPackages
from app.versionLister import versionnedPackages, saveExcel_versions
from app.treeMaker import addRootsOnBranches
from app.graph import makeJaalGraph


def highlightRepetitions(packages, requirements):
    for part in requirements.keys():
        print(part)
        found_included = 0
        for package in requirements[part].keys():
            full_package = package + '@' + requirements[part][package]
            if (full_package in packages.keys()):
                if ('roots' in packages[full_package]):
                    found_included += 1
                    print(f"\t {package} ({requirements[part][package]}) already imported in {packages[full_package]['roots']}")


def main():
    data = openFile()
    requirements = loadRequirements()
    packages, connections = detailledConnectPackages(data)
    v_packages = versionnedPackages(data, requirements)

    for depLevel in requirements.keys():
        saveExcel_versions(requirements[depLevel], depLevel, v_packages)

    # agglomerated = aglomerateAnyRootWithDetail(packages)
    for package in packages:
        packages = addRootsOnBranches(packages, package, 0, [])
    for package in packages:
        if ('roots' not in packages[package].keys()):
            packages[package]['isRoot'] = True

    highlightRepetitions(packages, requirements)
    print(len(list(packages.keys())))
    makeJaalGraph(packages, connections)
    # tree = buildTree(packages)


if __name__ == '__main__':
    main()
