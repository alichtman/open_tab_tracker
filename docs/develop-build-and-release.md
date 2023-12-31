# Developing, Building, and Releasing

`open-tab-tracker` uses [`hatch`](https://hatch.pypa.io/latest/) for dependency management, version management, building, and publishing.

## Cloning the repo for development

```bash
$ git clone git@github.com:alichtman/open_tab_tracker.git
$ cd open_tab_tracker
```

## Developing

From the repo root:

```bash
# Enter the virtual environment
$ hatch shell

# Install the package
$ pip3 install .

# Run it
$ open-tab-tracker -v
Open Tab Tracker v0.0.1
```

Make whatever changes you'd like, and re-run the `$ pip3 install` command to install the binary on your system.

## Adding Dependencies

Add your dependency manually to the `pyproject.toml` file and re-run `$ pip3 install .`.

## Building

From the project root:

```bash
$ hatch build .
```

## Bumping Version

`hatch` manages the versioning:

```bash
$ hatch version [ major / minor / patch ]
```

## Publishing

```bash
$ hatch publish
```
