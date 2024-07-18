# uninstalls packages in a poetry repot that have accidentally been installed globally

import subprocess

with open('poetry.lock', 'r') as file:
    packages = []
    for line in file:
        if 'name = "' in line:
            packages.append(line.split('"')[1])

for package in packages:
    subprocess.call(['pip', 'uninstall', '-y', package])
