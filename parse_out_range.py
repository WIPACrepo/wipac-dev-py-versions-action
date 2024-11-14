"""A script for parsing out ranges from python package metadata files."""

import os
import re

semver_range = ""
if os.path.isfile("pyproject.toml"):
    # ex: requires-python = ">=3.8, <3.13"
    pat = re.compile(r"requires-python = \"(?P<semver_range>[^\"]+)\"$")
    with open("pyproject.toml") as f:
        for line in f:
            if m := pat.match(line):
                semver_range = m.group("semver_range")
    if not semver_range:
        raise Exception("could not find `requires-python` entry in pyproject.toml")
elif os.path.isfile("setup.cfg"):
    # ex: python_requires = >=3.8, <3.13
    pat = re.compile(r"python_requires = (?P<semver_range>.+)$")
    with open("setup.cfg") as f:
        for line in f:
            if m := pat.match(line):
                semver_range = m.group("semver_range")
    if not semver_range:
        raise Exception("could not find `python_requires` entry in setup.cfg")
else:
    raise Exception("could not find pyproject.toml nor setup.cfg")

print(semver_range)
