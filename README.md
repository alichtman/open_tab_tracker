# open_tab_tracker.py

This tool tracks the count of open tabs you have, and plots them over time.

## Dependencies

-   [lz4json](https://github.com/andikleen/lz4json)
-   [jq](https://github.com/jqlang/jq)

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

-   Make a daemonized service that starts at login, and logs how many open tabs there are to the database every X minutes.
    -   https://github.com/prehensilecode/python-daemon-example/blob/master/eg_daemon.py
    -   https://peps.python.org/pep-3143/
-   Add support for Chrome, Chromium, and Safari. Need to add columns to the database to hold each new browser tab count
