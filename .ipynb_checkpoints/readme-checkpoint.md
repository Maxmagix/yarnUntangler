YarnUntangler v0.0.1

This tool is to help visualize package dependencies and relations in a project

It provides:
- excels of the different dependencies with target versions, current versions and latest version. for each devDependencies, peerDependencies and dependencies present in packages.json
- a repetition highlight that warns when packages in packages.json are already defined in others as dependencies of the yarn.lock
- an interactable graph to help visualize the connections between packages

It requires you to import a yarn.lock file and packages.json file at the root of the repo

You can use the jupyterNotebook for easier readability/choice of functions:

> brew install jupyterlab

> jupyter lab 

or run:

> ./venv/bin/pip3 install -r requirements.txt

> ./venv/bin/python3 main.py

but this will execute all the functions..