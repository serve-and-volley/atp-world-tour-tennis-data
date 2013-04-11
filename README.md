# ATP World Tour tennis data

This repository contains Python scripts that scrape tennis data from the <a href="http://www.atpworldtour.com/" target="_blank">ATP World Tour</a> website, as of April 2013. 
<br />
(Note: If the site does a redesign, then these scripts will no longer work.)

## Example
The following Python script: 

* <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/python/player_match_data.py" target="_blank">player_match_data.py</a>

collects all of the tournament and match stats for a single player, and exports the following example CSV file:

* <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/csv/Roger-Federer.csv" target="_blank">Roger-Federer.csv</a>

This file contains all data from the years 1998 through 2012 for Roger Federer. The following was the runtime for this example:

```
$ time python player_match_data.py
real  5m44.475s
user  0m39.638s
sys   0m3.563s
```

[Disclaimer: The code is the opposite of elegant, but it works; I will clean it up at some point.]
