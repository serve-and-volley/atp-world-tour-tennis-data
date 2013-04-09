This repository contains Python scripts that scrape tennis data from the <a href="http://www.atpworldtour.com/" target="_blank">ATP World Tour</a> website, as of April 2013. 
<br />
(Note: If the site does a redesign, then these scripts will no longer work.)

For example, the script: <br />
<a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/python/player_match_data.py" target="_blank">player_match_data.py</a>
<br />
[Disclaimer: the code is the opposite of elegant, but it works; I will clean it up at some point.]

collects all of the tournament and match stats for a single player. An example is the following CSV file: <br />
<a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/csv/Roger-Federer.csv" target="_blank">Roger-Federer.csv</a>

This file contains all data from the years 1998 through 2012. The following was the runtime to run the Python script and to generate the Federer CSV:

$ time python player_match_data.py

real  5m44.475s <br />
user	0m39.638s <br />
sys	0m3.563s <br />
