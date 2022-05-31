# WIPACrepo/wipac-dev-py-versions-action
GitHub Action Package for Generating a Build Matrix of Supported Python Versions for a Package

## Getting Started
`WIPACrepo/wipac-dev-py-versions-action` produces a JSON string containing a list/matrix of supported Python 3 versions by parsing a Python package's `setup.cfg`. The `python_requires` attribute (in the `[options]` section) is read and **must be in the format:** `python_requires = >=3.\d+, <3.\d+`. For example: `python_requires = >=3.6, <3.10`.
 
The JSON string is contained in the output variable `matrix`, and its versions are stored under the JSON key `'py3_versions'`. This action can be used to create a build matrix for running tests with different python versions. Below is a simple use case, where each version is used to run `pip install .`.


```
py-versions:
  runs-on: ubuntu-latest
  outputs:
    matrix: ${{ steps.versions.outputs.matrix }}
  steps:
    - uses: actions/checkout@v3
    - id: versions
      uses: WIPACrepo/wipac-dev-py-versions-action@v1

pip-install:
  needs: [py-versions]
  runs-on: ubuntu-latest
  strategy:
    max-parallel: 4
    fail-fast: false
    matrix: ${{ fromJSON(needs.py-versions.outputs.matrix) }}
  steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.py3_versions }}
    - run: |
        pip install --upgrade pip wheel setuptools
        pip install .
```
