# open-tab-tracker.py

This tool tracks the count of open tabs you have, and plots them over time.

## Dependencies

-   [lz4json](https://github.com/andikleen/lz4json)
-   [jq](https://github.com/jqlang/jq)

## Installation

This package has not been released anywhere, so you'll have to run it by cloning the git repo:

```bash
$ git clone git@github.com:alichtman/open-tab-tracker.git
$ cd open-tab-tracker
$ python3 open-tab-tracker.py
```

## TODO

-   Make a daemonized service that runs every X minutes, and logs how many open tabs there are
-   Store the data in some database
-   Display the data in some pretty graph
-   Add support for Chrome, Chromium, and Safari
