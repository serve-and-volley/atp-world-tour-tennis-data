# ATP World Tour tennis data

This repository contains Python scripts that scrape tennis data from the <a href="http://www.atpworldtour.com/" target="_blank">ATP World Tour</a> website, as of April 2013. 
<br />
(Note: If the site does a redesign, then these scripts will no longer work.)

## Example
The following Python script: 

* <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/python/player_match_data.py" target="_blank">player_match_data.py</a>

collects all of the tournament and match stats for a single player, and exports the following example CSV file:

* <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/csv/John-Mcenroe.csv" target="_blank">John-Mcenroe.csv</a>

This file contains all data from the years 1976 through 1992 for John McEnroe. The Python script takes input arguments from the command line, so for this example it would be:

```
$ python player_match_data.py John-Mcenroe 1976 1992 retired
```

The following was the runtime for this example:

```
$ time python player_match_data.py
real    7m20.479s
user    0m36.934s
sys     0m3.391s
```

[Disclaimer: The code is the opposite of elegant, but it works; I will be cleaning it up at some point in the hopes of improving the runtime.]