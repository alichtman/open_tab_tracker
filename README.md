# open_tab_tracker.py

This tool tracks the count of open tabs you have, and plots them over time.

## Dependencies

-   [lz4json](https://github.com/andikleen/lz4json)
-   [jq](https://github.com/jqlang/jq)

I built a `so` for lz4json [from here](https://github.com/alichtman/lz4json/tree/master) with `$ make lz4jsoncat.so`, and have included it in this repo.

## Installation

This package has not been released anywhere, so you'll have to run it by cloning the git repo:

```bash
$ git clone git@github.com:alichtman/open_tab_tracker.git
$ cd open_tab_tracker
$ poetry install
$ poetry shell
$ python3 -m open_tab_tracker
```

## Technical Details

Data is stored in a `sqlite3` database at `$XDG_DATA_HOME/open_tab_tracker.db`.

## TODO

-   Get crontab running. lz4jsoncat needs to be installed when this package is installed
-   Add support for Chrome, Chromium, and Safari. Need to add columns to the database to hold each new browser tab count
