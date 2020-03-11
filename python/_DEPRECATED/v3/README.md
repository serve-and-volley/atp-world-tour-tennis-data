<div id="contents"></div>

# ATP World Tour tennis data

This repository contains Python scripts that scrape tennis data from the <a href="http://www.atpworldtour.com/" target="_blank">ATP World Tour</a> website, as of July 2017. Note that if the site layout is subsequently redesigned, then these scripts will no longer work.

## Contents
- A. [Scraping tournament data by year](#part-a)
  - A1.  [The `tournaments.py` script](#part-a1)
  - A2. [Example usage](#part-a2)
- B. [Scraping match scores for each tournament](#part-b)
  - B1. [The `match_scores.py` script](#part-b1)
  - B2. [Example usage](#part-b2)
- C. [Scraping match stats for each match](#part-c)
  - C1. [The `match_stats.py` script](#part-c1)
  - C2. [Example usage](#part-c2)
  - C3. [Asynchronous scraping issues](#part-c3)

<div id="part-a"></div>

## A. Scraping tournament data by year

<div id="part-a1"></div>

### A1. The `tournaments.py` script [^](#contents)
The following Python script:
* <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/python/tournaments.py" target="_blank">tournaments.py</a>

scrapes the following data:
```
tourney_year
tourney_order
tourney_name
tourney_id
tourney_slug
tourney_location
tourney_dates
tourney_singles_draw
tourney_doubles_draw
tourney_conditions
tourney_surface
tourney_fin_commit
tourney_url_suffix
singles_winner_name
singles_winner_url
singles_winner_player_slug
singles_winner_player_id
doubles_winner_1_name
doubles_winner_1_url
doubles_winner_1_player_slug
doubles_winner_1_player_id
doubles_winner_2_name
doubles_winner_2_url
doubles_winner_2_player_slug
doubles_winner_2_player_id
```
from pages like the following:
* http://www.atpworldtour.com/en/scores/results-archive?year=2016

![image](https://user-images.githubusercontent.com/532545/28861915-f76a5dfa-7717-11e7-85cd-696e62627971.png)

The CSV file for all tournament data from 1877-2016 is found in:
* https://github.com/serve-and-volley/atp-world-tour-tennis-data/tree/master/csv/1_tournaments

<div id="part-a2"></div>

### A2. Example usage [^](#contents)
Example command line usage and output is as follows:
```
$ time python tournaments.py 2012 2016

Year    Tournaments
----    -----------
2012    67
2013    65
2014    64
2015    66
2016    67

real	0m8.617s
user	0m0.675s
sys	0m0.062s
```

<div id="part-b"></div>

## B. Scraping match scores for each tournament

<div id="part-b1"></div>

### B1. The `match_scores.py` script [^](#contents)
The following Python script:
* <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/python/match_scores.py" target="_blank">match_scores.py</a>

scrapes the following data:
```
match_year
tourney_order
tourney_name
tourney_id
tourney_slug
tourney_location
tourney_dates
tourney_singles_draw
tourney_doubles_draw
tourney_conditions
tourney_surface
tourney_fin_commit
tourney_long_slug
tourney_round_name
round_order
match_order
winner_name
winner_player_id
winner_slug
loser_name
loser_player_id
loser_slug
match_score
match_stats_url_suffix
```

from pages like the following:
* http://www.atpworldtour.com/en/scores/archive/wimbledon/540/2016/results

![image](https://user-images.githubusercontent.com/532545/28890551-4f2793e6-777c-11e7-9497-a6bedafdad06.png)

The CSV files for all match scores data from 1877-2016 is found in:
* https://github.com/serve-and-volley/atp-world-tour-tennis-data/tree/master/csv/2_match_scores

<div id="part-b2"></div>

### B2. Example usage [^](#contents)
Example command line usage and output is as follows:
```
$ time python match_scores.py 1967 1968

Scraping match info for 4 tournaments...
Year    Order    Tournament                                Matches
----    -----    ----------                                -------
1967    1        Australian Championships                  58
1967    2        French Championships                      123
1967    3        Wimbledon                                 127
1967    4        US Championships                          127

Scraping match info for 13 tournaments...
Year    Order    Tournament                                Matches
----    -----    ----------                                -------
1968    1        Australian Chps.                          61
1968    2        Bournemouth                               31
1968    3        Roland Garros                             127
1968    4        Beckenham                                 43
1968    5        London / Queen's Club                     53
1968    6        Wimbledon                                 127
1968    7        Dublin                                    31
1968    8        Gstaad                                    31
1968    9        Montreal / Toronto                        0
1968    10       Hamburg                                   47
1968    11       US Open                                   95
1968    12       Los Angeles                               68
1968    13       Buenos Aires                              36

real	0m21.406s
user	0m0.810s
sys	0m0.099s
```

<div id="part-c"></div>

## C. Scraping match stats for each match

<div id="part-c1"></div>

### C1. The `match_stats.py` script [^](#contents)
The following Python script:
* <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/python/match_stats.py" target="_blank">match_stats.py</a>

scrapes the following data:
```
match_url_suffix
match_time
match_duration
winner_aces
winner_double_faults
winner_first_serves_in
winner_first_serves_total
winner_first_serve_points_won
winner_first_serve_points_total
winner_second_serve_points_won
winner_second_serve_points_total
winner_break_points_saved
winner_break_points_serve_total
winner_service_points_won
winner_service_points_total
winner_first_serve_return_won
winner_first_serve_return_total
winner_second_serve_return_won
winner_second_serve_return_total
winner_break_points_converted
winner_break_points_return_total
winner_service_games_played
winner_return_games_played
winner_return_points_won
winner_return_points_total
winner_total_points_won
winner_total_points_total
loser_aces
loser_double_faults
loser_first_serves_in
loser_first_serves_total
loser_first_serve_points_won
loser_first_serve_points_total
loser_second_serve_points_won
loser_second_serve_points_total
loser_break_points_saved
loser_break_points_serve_total
loser_service_points_won
loser_service_points_total
loser_first_serve_return_won
loser_first_serve_return_total
loser_second_serve_return_won
loser_second_serve_return_total
loser_break_points_converted
loser_break_points_return_total
loser_service_games_played
loser_return_games_played
loser_return_points_won
loser_return_points_total
loser_total_points_won
loser_total_points_total
```

from pages like the following:
* http://www.atpworldtour.com/en/tournaments/australian-open/580/2017/match-stats/F324/N409/live/MS001/match-stats

The CSV files for all match stats data from 1991-2016 is found in:
* https://github.com/serve-and-volley/atp-world-tour-tennis-data/tree/master/csv/3_match_stats

[Note: the ATP did not start keeping match stats data until 1991.]

<div id="part-c2"></div>

### C2. Example usage [^](#contents)

#### C2a. Example error 1: Connection error
Example command line usage and output is as follows, with the resulting connection error:
```
$ time python match_stats.py 2012 31

Collecting match stats data for 66 tournaments:

Index    Tourney slug       Matches
-----    ------------       -------
31       roland-garros      239/239 (100%)
32       halle              29/47 (62%)Traceback (most recent call last):
  File "match_stats.py", line 51, in <module>
    match_stats_data_scrape += asynchronous(match_stats_url_suffixes, scrape_match_stats, tourney_index, tourney_slug)
  File "/Users/kevin/Desktop/atp_scrape/final/functions.py", line 567, in asynchronous
    scrape_match_stats_output += future.result()
  File "/Library/Python/2.7/site-packages/concurrent/futures/_base.py", line 422, in result
    return self.__get_result()
  File "/Library/Python/2.7/site-packages/concurrent/futures/_base.py", line 381, in __get_result
    raise exception_type, self._exception, self._traceback
requests.exceptions.ConnectionError: None: Max retries exceeded with url: /en/tournaments/gerry-weber-open/500/2012/match-stats/k776/bg52/match-stats (Caused by redirect)

real	0m25.230s
user	0m3.706s
sys	0m0.827s
```
When this happens, I recommend waiting for ~5 minutes before running the script starting on the index of the tournament that didn't reach 100% completion in scraping.

#### C2b. Example error 2: Parsing error
Example command line usage and output is as follows, with the resulting parsing error:
```
$ time python match_stats.py 2013 0

Collecting match stats data for 64 tournaments:

Index    Tourney slug       Matches
-----    ------------       -------
0        brisbane           55/55 (100%)
1        chennai            55/55 (100%)
2        doha               59/59 (100%)
3        auckland           53/53 (100%)
4        sydney             55/55 (100%)
5        australian-open    239/239 (100%)
6        montpellier        55/55 (100%)
7        vina-del-mar       54/54 (100%)
8        zagreb             55/55 (100%)
9        rotterdam          43/43 (100%)
10       san-jose           55/55 (100%)
11       sao-paulo          55/55 (100%)
12       buenos-aires       59/59 (100%)
13       marseille          55/55 (100%)
14       memphis            42/42 (100%)
15       acapulco           43/43 (100%)
16       delray-beach       28/59 (47%)Exception in thread Thread-17:
Traceback (most recent call last):
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 808, in __bootstrap_inner
    self.run()
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 761, in run
    self.__target(*self.__args, **self.__kwargs)
  File "/Library/Python/2.7/site-packages/concurrent/futures/process.py", line 208, in _queue_management_worker
    result_item = result_queue.get(block=True)
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/multiprocessing/queues.py", line 117, in get
    res = self._recv()
  File "parser.pxi", line 18, in lxml.etree.ParseError.__init__ (src/lxml/lxml.etree.c:80812)
TypeError: ('__init__() takes exactly 5 positional arguments (2 given)', <class 'lxml.etree.XMLSyntaxError'>, (u'line 1672: Element script embeds close tag',))

^Z
[1]+  Stopped                 python match_stats.py 2013 0

real	2m46.015s
user	0m0.000s
sys	0m0.001s
```

<div id="part-c3"></div>

For errors like this you will need to kill the process id's before resuming scraping on the index of the tournament that didn't reach 100% completion in scraping.

### C3. Asynchronous scraping issues [^](#contents)

Because this script scrapes asynchronously (you can adjust the max number of workers in the <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/python/functions.py#L560" target="_blank">functions.py</a> file), you will run into connection problems as the ATP servers are being hammered by the script. Always remember to kill the process id (PID) after you are forced to stop the script, for example:

```
$ ps
  PID TTY           TIME CMD
30062 ttys000    0:00.46 -bash
34562 ttys000    0:01.59 python match_stats.py 2013 0
34734 ttys000    0:00.09 python match_stats.py 2013 0
34735 ttys000    0:00.07 python match_stats.py 2013 0
34736 ttys000    0:00.09 python match_stats.py 2013 0
34737 ttys000    0:00.09 python match_stats.py 2013 0
34738 ttys000    0:00.09 python match_stats.py 2013 0
34739 ttys000    0:00.07 python match_stats.py 2013 0
34740 ttys000    0:00.09 python match_stats.py 2013 0
34741 ttys000    0:00.09 python match_stats.py 2013 0
34742 ttys000    0:00.09 python match_stats.py 2013 0
34743 ttys000    0:00.09 python match_stats.py 2013 0
30066 ttys001    0:00.03 -bash
30140 ttys002    0:00.01 -bash
30144 ttys002    0:00.05 /Applications/Postgres.app/Contents/Versions/9.3/bin/psql -p5432

$ kill 34562
[1]+  Terminated: 15          python match_stats.py 2013 0

$ ps
  PID TTY           TIME CMD
30062 ttys000    0:00.46 -bash
30066 ttys001    0:00.03 -bash
30140 ttys002    0:00.01 -bash
30144 ttys002    0:00.05 /Applications/Postgres.app/Contents/Versions/9.3/bin/psql -p5432
```
