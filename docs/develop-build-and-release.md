# Developing, Building, and Releasing

`open_tab_tracker` uses [`hatch`](https://hatch.pypa.io/latest/) for dependency management, version management, building, and publishing.

## Developing

```bash
$ git clone git@github.com:alichtman/open_tab_tracker.git
$ cd open_tab_tracker
$ pip3 install .
$ open-tab-tracker -v
Open Tab Tracker v0.0.1
```

Make whatever changes you'd like, and re-run the `$ pip3 install` command to install the binary on your system.

## Building

From the project root:

```bash
$ hatch build .
```

## Bumping Version

We are managing versioning with `hatch`.

```bash
$ hatch version [ major / minor / patch ]
```

## Publishing

```bash
$ hatch publish
```
