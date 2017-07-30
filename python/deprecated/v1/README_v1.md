#### [Note: This is the deprecated `README.md` file for the deprecated `player_match_data.py` script]

# ATP World Tour tennis data

This repository contains Python scripts that scrape tennis data from the <a href="http://www.atpworldtour.com/" target="_blank">ATP World Tour</a> website, as of April 2013. 
<br />
(Note: If the site does a redesign, then these scripts will no longer work.)

## Example
The following Python script: 

* <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/python/deprecated/v1/player_match_data.py" target="_blank">player_match_data.py</a>

collects all of the tournament and match stats for a single player, and exports the following example CSV file:

* <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/csv/previous_versions/retired_players/Jimmy-Connors.csv" target="_blank">Jimmy-Connors.csv</a> (545 KB)

This file contains all data from the active years of 1970 through 1996 for Jimmy Connors, who had the longest career out of anyone in the Open Era (post-1968). The Python script takes input arguments from the command line, so for this example it would be:

```
$ python player_match_data.py Jimmy-Connors 1970 1996 retired
```

The following was the runtime for this example:

```
$ time python player_match_data.py Jimmy-Connors 1970 1996 retired
real    12m43.512s
user    0m48.475s
sys     0m3.845s
```

[Disclaimer: The code is the opposite of elegant, but it works; I will be cleaning it up at some point in the hopes of improving the runtime.]
