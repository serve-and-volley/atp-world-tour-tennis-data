<div id="contents"></div>

# ATP World Tour tennis data

This repository contains Python scripts that scrape tennis data from the <a href="http://www.atpworldtour.com/" target="_blank">ATP World Tour</a> website, as of October 2017. Note that if the site layout is subsequently redesigned, then these scripts will no longer work.

### License
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

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
tourney_year_id
tourney_order
tourney_type
tourney_name
tourney_id
tourney_slug
tourney_location
tourney_date
year
tourney_month
tourney_day
tourney_singles_draw
tourney_doubles_draw
tourney_conditions
tourney_surface
tourney_fin_commit_raw
currency
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
* https://www.atptour.com/en/scores/results-archive?year=2019

![image](https://user-images.githubusercontent.com/532545/74613783-6e7f7f80-50df-11ea-9f70-7860e4696c6f.png)

The CSV file for all tournament data from 1877-2016 is found in:
* https://github.com/serve-and-volley/atp-world-tour-tennis-data/tree/master/csv/1_tournaments

<div id="part-a2"></div>

### A2. Example usage [^](#contents)
Example command line usage and output is as follows:
```
$ time python3 tournaments.py 2010 2019

Year    Tournaments
----    -----------
2010    66
2011    66
2012    67
2013    65
2014    65
2015    66
2016    67
2017    69
2018    69
2019    68

real	0m14.230s
user	0m7.306s
sys	0m0.104s
```

<div id="part-b"></div>

## B. Scraping match scores for each tournament

<div id="part-b1"></div>

### B1. The `match_scores.py` script [^](#contents)
The following Python script:
* <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/python/match_scores.py" target="_blank">match_scores.py</a>

scrapes the following data:
```
tourney_year_id
tourney_order
tourney_name
tourney_slug
tourney_url_suffix
start_date
start_year
start_month
start_day
end_date
end_year
end_month
end_day
currency
prize_money
match_index
tourney_round_name
round_order
match_order
winner_name
winner_player_id
winner_slug
loser_name
loser_player_id
loser_slug
winner_seed
loser_seed
match_score_tiebreaks
winner_sets_won
loser_sets_won
winner_games_won
loser_games_won
winner_tiebreaks_won
loser_tiebreaks_won
match_id
match_stats_url_suffix
```

from pages like the following:
* https://www.atptour.com/en/scores/archive/australian-open/580/2019/results

![image](https://user-images.githubusercontent.com/532545/74780146-ffd02c80-526c-11ea-9bea-360bfbd965ff.png)

The CSV files for all match scores data from 1877-2016 is found in:
* https://github.com/serve-and-volley/atp-world-tour-tennis-data/tree/master/csv/2_match_scores

<div id="part-b2"></div>

### B2. Example usage [^](#contents)
Example command line usage and output is as follows:
```
$ time python3 match_scores.py 1967 1968

Scraping match info for 4 tournaments...
Year    Order    Tournament                                Matches
----    -----    ----------                                -------
1967    1        australian-championships                  58
1967    2        french-championships                      123
1967    3        wimbledon                                 127
1967    4        us-championships                          127

Scraping match info for 15 tournaments...
Year    Order    Tournament                                Matches
----    -----    ----------                                -------
1968    1        australian-chps                           61
1968    2        bournemouth                               31
1968    3        rome                                      103
1968    4        roland-garros                             126
1968    5        barcelona                                 57
1968    6        london                                    53
1968    7        wimbledon                                 127
1968    8        cincinnati                                11
1968    9        dublin                                    31
1968    10       gstaad                                    31
1968    11       hamburg                                   47
1968    12       toronto                                   0
1968    13       us-open                                   95
1968    14       los-angeles                               68
1968    15       buenos-aires                              36

real    0m21.037s
user    0m8.330s
sys     0m0.211s
```

<div id="part-c"></div>

## C. Scraping match stats for each match

<div id="part-c1"></div>

### C1. The `match_stats.py` script [^](#contents)
The following Python script:
* <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/python/match_stats.py" target="_blank">match_stats.py</a>

scrapes the following data:
```
match_id
tourney_slug
match_stats_url_suffix
match_time
match_duration
winner_slug
winner_serve_rating
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
winner_service_games_played
winner_return_rating
winner_first_serve_return_won
winner_first_serve_return_total
winner_second_serve_return_won
winner_second_serve_return_total
winner_break_points_converted
winner_break_points_return_total
winner_return_games_played
winner_service_points_won
winner_service_points_total
winner_return_points_won
winner_return_points_total
winner_total_points_won
winner_total_points_total
loser_slug
loser_serve_rating
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
loser_service_games_played
loser_return_rating
loser_first_serve_return_won
loser_first_serve_return_total
loser_second_serve_return_won
loser_second_serve_return_total
loser_break_points_converted
loser_break_points_return_total
loser_return_games_played
loser_service_points_won
loser_service_points_total
loser_return_points_won
loser_return_points_total
loser_total_points_won
loser_total_points_total
```

from pages like the following:
* http://www.atpworldtour.com/en/scores/2017/580/MS001/match-stats

![image](https://user-images.githubusercontent.com/532545/76129824-8bb8b700-5fd6-11ea-9eea-ac60c5d5942d.png)

The CSV files for all match stats data from 1991-2016 is found in:
* https://github.com/serve-and-volley/atp-world-tour-tennis-data/tree/master/csv/3_match_stats

[Note: the ATP did not start keeping match stats data until 1991.]

<div id="part-c2"></div>

### C2. Example usage [^](#contents)
Example command line usage and output is as follows:
```
$ time python3 match_stats.py 1991

Collecting match stats data for 83 tournaments:

Index    Tourney slug           Matches
-----    ------------           -------
0        adelaide               30/30 (100%)
1        wellington             30/30 (100%)
2        sydney                 31/31 (100%)
3        auckland               29/29 (100%)
4        australian-open        127/127 (100%)
5        milan                  29/31 (94%)
6        san-francisco          30/31 (97%)
7        guaruja                30/31 (97%)
8        philadelphia           47/47 (100%)
9        brussels               31/31 (100%)
10       stuttgart              31/31 (100%)
11       memphis                47/47 (100%)
12       rotterdam              31/31 (100%)
13       chicago                30/30 (100%)
14       indian-wells           54/54 (100%)
15       copenhagen             31/31 (100%)
16       miami                  95/95 (100%)
17       estoril                31/31 (100%)
18       hong-kong              31/31 (100%)
19       orlando                31/31 (100%)
20       tokyo                  53/54 (98%)
21       barcelona              54/54 (100%)
22       nice                   31/31 (100%)
23       seoul                  31/31 (100%)
24       monte-carlo            54/54 (100%)
25       singapore              31/31 (100%)
26       madrid                 31/31 (100%)
27       munich                 31/31 (100%)
28       tampa                  29/30 (97%)
29       hamburg                55/55 (100%)
30       charlotte              1/30 (3%)
31       rome                   59/59 (100%)
32       umag                   29/31 (94%)
33       dusseldorf             Match structure/stats URL problem
34       bologna                30/30 (100%)
35       roland-garros          47/47 (100%)
36       london                 53/53 (100%)
37       florence               30/31 (97%)
38       rosmalen               31/31 (100%)
39       genova                 31/31 (100%)
40       manchester             31/31 (100%)
41       wimbledon              121/121 (100%)
42       gstaad                 30/30 (100%)
43       bastad                 31/31 (100%)
44       newport                29/31 (94%)
45       stuttgart              47/47 (100%)
46       washington             55/55 (100%)
47       montreal               55/55 (100%)
48       hilversum              30/30 (100%)
49       kitzbuhel              47/47 (100%)
50       los-angeles            31/31 (100%)
51       san-marino             29/30 (97%)
52       cincinnati             55/55 (100%)
53       prague                 30/31 (97%)
54       indianapolis           55/55 (100%)
55       new-haven              54/54 (100%)
56       long-island            31/31 (100%)
57       schenectady            30/31 (97%)
58       us-open                125/125 (100%)
59       bordeaux               31/31 (100%)
60       brasilia               46/47 (98%)
61       geneva                 31/31 (100%)
62       basel                  31/31 (100%)
63       palermo                31/31 (100%)
64       brisbane               30/31 (97%)
65       sydney                 47/47 (100%)
66       toulouse               31/31 (100%)
67       athens                 30/31 (97%)
68       tokyo                  45/47 (96%)
69       berlin                 31/31 (100%)
70       tel-aviv               30/31 (97%)
71       lyon                   31/31 (100%)
72       vienna                 31/31 (100%)
73       stockholm              47/47 (100%)
74       guaruja                31/31 (100%)
75       paris                  46/46 (100%)
76       buzios                 31/31 (100%)
77       birmingham             31/31 (100%)
78       moscow                 30/30 (100%)
79       sao-paulo              29/29 (100%)
80       atp-tour-world-championship    1/1 (100%)
81       atp-tour-world-doubles-championship    Match structure/stats URL problem
82       munich                 Match structure/stats URL problem

real	36m11.241s
user	2m13.432s
sys	  0m4.073s
```
