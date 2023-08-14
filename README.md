<div id="contents"></div>

# ATP World Tour tennis data

This repository contains Python scripts that scrape tennis data from the <a href="http://www.atpworldtour.com/" target="_blank">ATP World Tour</a> website, as of August 2023. Note that if the site layout is subsequently redesigned, then these scripts will no longer work.

### License
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

## Contents
- A. [Scraping tournament data by year](#part-a)
  - A1.  [The `tournaments.py` script](#part-a1)
  - A2. [Example usage](#part-a2)
- B. [Scraping match scores for each tournament](#part-b)
  - B1. [The `match_scores.py` script](#part-b1)
  - B2. [Example usage](#part-b2)
- C. [Scraping match stats for matches on and after 2021-10-18 (Moscow ATP 250)](#part-c)
  - C1. [The `match_stats.py` script](#part-c1)
  - C2. [Example usage](#part-c2)

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

## C. Scraping match stats for all Grand Slam matches and ATP matches before 2021-10-18 (Moscow ATP 250)
<div id="part-d1"></div>

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
as well as the following **extended data**:
```
match_id
tourney_slug
match_stats_url_suffix
winner_player_id
winner_net_points_won
winner_net_points_total
winner_winners
winner_unforced_errors
winner_max_service_speed_kmh
winner_max_service_speed_mph
winner_avg_1st_serve_speed_kmh
winner_avg_1st_serve_speed_mph
winner_avg_2nd_serve_speed_kmh
winner_avg_2nd_serve_speed_mph
loser_player_id
loser_net_points_won
loser_net_points_total
loser_winners
loser_unforced_errors
loser_max_service_speed_kmh
loser_max_service_speed_mph
loser_avg_1st_serve_speed_kmh
loser_avg_1st_serve_speed_mph
loser_avg_2nd_serve_speed_kmh
loser_avg_2nd_serve_speed_mph
```

from pages like the following:
* [https://www.atptour.com/en/scores/stats-centre/archive/2023/2843/ms001](https://www.atptour.com/en/scores/stats-centre/archive/2023/2843/ms001)

![image](https://github.com/serve-and-volley/atp-world-tour-tennis-data/assets/532545/deda55d1-2f7e-4936-80f4-d321b0fa57da)

The CSV files for all match stats data from 1991-2022 is found in:
* https://github.com/serve-and-volley/atp-world-tour-tennis-data/tree/master/csv/3_match_stats

[Note: the ATP did not start keeping match stats data until 1991.]

<div id="part-c2"></div>

### C1. Example usage [^](#contents)
Example command line usage and output is as follows:
```
$ time python3 match_stats.py

Enter year: 2023

67/50 tournament stats available

 1 - 2022.12.29 - United Cup
 2 - 2023.01.01 - Adelaide International 1
 3 - 2023.01.02 - Tata Open Maharashtra
 4 - 2023.01.09 - ASB Classic
 5 - 2023.01.09 - Adelaide International 2
 6 - 2023.01.16 - Australian Open
 7 - 2023.02.06 - Dallas Open
 8 - 2023.02.06 - Cordoba Open
 9 - 2023.02.06 - Open Sud de France – Montpellier
10 - 2023.02.13 - ABN AMRO Open
11 - 2023.02.13 - Delray Beach Open
12 - 2023.02.13 - Argentina Open
13 - 2023.02.20 - Rio Open presented by Claro
14 - 2023.02.20 - Qatar ExxonMobil Open
15 - 2023.02.20 - Open 13 Provence
16 - 2023.02.27 - Dubai Duty Free Tennis Championships
17 - 2023.02.27 - Abierto Mexicano Telcel presentado por HSBC
18 - 2023.02.27 - Movistar Chile Open
19 - 2023.03.08 - BNP Paribas Open
20 - 2023.03.22 - Miami Open presented by Itau
21 - 2023.04.03 - Fayez Sarofim & Co. U.S. Men's Clay Court Championship
22 - 2023.04.03 - Grand Prix Hassan II
23 - 2023.04.03 - Millennium Estoril Open
24 - 2023.04.09 - Rolex Monte-Carlo Masters
25 - 2023.04.17 - Barcelona Open Banc Sabadell
26 - 2023.04.17 - BMW Open by American Express
27 - 2023.04.17 - Srpska Open
28 - 2023.04.26 - Mutua Madrid Open
29 - 2023.05.10 - Internazionali BNL d'Italia
30 - 2023.05.21 - Gonet Geneva Open
31 - 2023.05.21 - Open Parc Auvergne-Rhone-Alpes Lyon
32 - 2023.05.28 - Roland Garros
33 - 2023.06.12 - BOSS OPEN
34 - 2023.06.12 - Libema Open
35 - 2023.06.19 - Cinch Championships
36 - 2023.06.19 - Terra Wortmann Open
37 - 2023.06.24 - Mallorca Championships
38 - 2023.06.26 - Rothesay International
39 - 2023.07.03 - Wimbledon
40 - 2023.07.17 - Infosys Hall of Fame Open
41 - 2023.07.17 - EFG Swiss Open Gstaad
42 - 2023.07.17 - Nordea Open
43 - 2023.07.24 - Hamburg European Open
44 - 2023.07.24 - Atlanta Open
45 - 2023.07.24 - Plava Laguna Croatia Open Umag
46 - 2023.07.31 - Mubadala Citi DC Open
47 - 2023.07.31 - Mifel Tennis Open by Telcel Oppo
48 - 2023.07.31 - Generali Open
49 - 2023.08.07 - National Bank Open Presented by Rogers
50 - 2023.08.13 - Western & Southern Open
51 - 2023.08.20 - Winston-Salem Open
52 - 2023.08.28 - US Open
53 - 2023.09.20 - Chengdu Open
54 - 2023.09.20 - Zhuhai Championships
55 - 2023.09.22 - Laver Cup
56 - 2023.09.27 - Astana Open
57 - 2023.09.28 - China Open
58 - 2023.10.04 - Rolex Shanghai Masters
59 - 2023.10.16 - Kinoshita Group Japan Open Tennis Championships
60 - 2023.10.16 - BNP Paribas Nordic Open
61 - 2023.10.16 - European Open
62 - 2023.10.23 - Erste Bank Open
63 - 2023.10.23 - Swiss Indoors Basel
64 - 2023.10.30 - Rolex Paris Masters
65 - 2023.11.05 - Moselle Open
66 - 2023.11.05 - Tel Aviv Watergen Open
67 - 2023.11.12 - Nitto ATP Finals

Enter tourney number: 2

1 - adelaide - 2023-2843-ms001-7-1-d643-k0ah - Final
2 - adelaide - 2023-2843-ms002-6-2-d643-mm58 - Semifinals
3 - adelaide - 2023-2843-ms003-6-1-k0ah-n732 - Semifinals
4 - adelaide - 2023-2843-ms004-5-4-d643-su55 - Quarterfinals
5 - adelaide - 2023-2843-ms005-5-3-mm58-ke29 - Quarterfinals
6 - adelaide - 2023-2843-ms006-5-2-k0ah-s0ag - Quarterfinals
7 - adelaide - 2023-2843-ms007-5-1-n732-p09z - Quarterfinals
8 - adelaide - 2023-2843-ms008-4-8-d643-hb64 - Round of 16
9 - adelaide - 2023-2843-ms010-4-7-mm58-ki95 - Round of 16
10 - adelaide - 2023-2843-ms012-4-6-s0ag-kd46 - Round of 16
11 - adelaide - 2023-2843-ms009-4-5-su55-sx50 - Round of 16
12 - adelaide - 2023-2843-ms011-4-4-ke29-d0co - Round of 16
13 - adelaide - 2023-2843-ms013-4-3-k0ah-bd06 - Round of 16
14 - adelaide - 2023-2843-ms014-4-2-n732-mk66 - Round of 16
15 - adelaide - 2023-2843-ms015-4-1-p09z-gc88 - Round of 16
16 - adelaide - 2023-2843-ms016-3-16-d643-lb66 - Round of 32
17 - adelaide - 2023-2843-ms031-3-15-p09z-ag37 - Round of 32
18 - adelaide - 2023-2843-ms020-3-14-mm58-su87 - Round of 32
19 - adelaide - 2023-2843-ms027-3-13-bd06-re44 - Round of 32
20 - adelaide - 2023-2843-ms028-3-12-n732-r0dg - Round of 32
21 - adelaide - 2023-2843-ms024-3-11-s0ag-e831 - Round of 32
22 - adelaide - 2023-2843-ms019-3-10-su55-h0bh - Round of 32
23 - adelaide - 2023-2843-ms023-3-9-ke29-cg04 - Round of 32
24 - adelaide - 2023-2843-ms022-3-8-d0co-kf17 - Round of 32
25 - adelaide - 2023-2843-ms030-3-7-gc88-g628 - Round of 32
26 - adelaide - 2023-2843-ms017-3-6-hb64-tc61 - Round of 32
27 - adelaide - 2023-2843-ms021-3-5-ki95-o483 - Round of 32
28 - adelaide - 2023-2843-ms025-3-4-kd46-c0bc - Round of 32
29 - adelaide - 2023-2843-ms026-3-3-k0ah-mc10 - Round of 32
30 - adelaide - 2023-2843-ms029-3-2-mk66-ge33 - Round of 32
31 - adelaide - 2023-2843-ms018-3-1-sx50-y268 - Round of 32
32 - adelaide - 2023-2843-qs004-2-4-kf17-da81 - 2nd Round Qualifying
33 - adelaide - 2023-2843-qs006-2-3-sx50-pd07 - 2nd Round Qualifying
34 - adelaide - 2023-2843-qs007-2-2-h0bh-d994 - 2nd Round Qualifying
35 - adelaide - 2023-2843-qs005-2-1-p09z-wb32 - 2nd Round Qualifying
36 - adelaide - 2023-2843-qs008-1-8-kf17-tb69 - 1st Round Qualifying
37 - adelaide - 2023-2843-qs010-1-7-wb32-hh26 - 1st Round Qualifying
38 - adelaide - 2023-2843-qs012-1-6-sx50-h997 - 1st Round Qualifying
39 - adelaide - 2023-2843-qs014-1-5-h0bh-bk24 - 1st Round Qualifying
40 - adelaide - 2023-2843-qs009-1-4-da81-w0c4 - 1st Round Qualifying
41 - adelaide - 2023-2843-qs015-1-3-d994-s0s1 - 1st Round Qualifying
42 - adelaide - 2023-2843-qs013-1-2-pd07-mh30 - 1st Round Qualifying
43 - adelaide - 2023-2843-qs011-1-1-p09z-z371 - 1st Round Qualifying

Enter match to start scraping: 1

WARNING:root:Can not find chromedriver for currently installed chrome version.
1 - adelaide - 2023-2843-ms001-7-1-d643-k0ah - Final (plus extended data)
2 - adelaide - 2023-2843-ms002-6-2-d643-mm58 - Semifinals
3 - adelaide - 2023-2843-ms003-6-1-k0ah-n732 - Semifinals
4 - adelaide - 2023-2843-ms004-5-4-d643-su55 - Quarterfinals
5 - adelaide - 2023-2843-ms005-5-3-mm58-ke29 - Quarterfinals
6 - adelaide - 2023-2843-ms006-5-2-k0ah-s0ag - Quarterfinals
7 - adelaide - 2023-2843-ms007-5-1-n732-p09z - Quarterfinals
8 - adelaide - 2023-2843-ms008-4-8-d643-hb64 - Round of 16
9 - adelaide - 2023-2843-ms010-4-7-mm58-ki95 - Round of 16
10 - adelaide - 2023-2843-ms012-4-6-s0ag-kd46 - Round of 16
11 - adelaide - 2023-2843-ms009-4-5-su55-sx50 - Round of 16
12 - adelaide - 2023-2843-ms011-4-4-ke29-d0co - Round of 16
13 - adelaide - 2023-2843-ms013-4-3-k0ah-bd06 - Round of 16
14 - adelaide - 2023-2843-ms014-4-2-n732-mk66 - Round of 16
15 - adelaide - 2023-2843-ms015-4-1-p09z-gc88 - Round of 16
16 - adelaide - 2023-2843-ms016-3-16-d643-lb66 - Round of 32
17 - adelaide - 2023-2843-ms031-3-15-p09z-ag37 - Round of 32
18 - adelaide - 2023-2843-ms020-3-14-mm58-su87 - Round of 32
19 - adelaide - 2023-2843-ms027-3-13-bd06-re44 - Round of 32
20 - adelaide - 2023-2843-ms028-3-12-n732-r0dg - Round of 32
21 - adelaide - 2023-2843-ms024-3-11-s0ag-e831 - Round of 32
22 - adelaide - 2023-2843-ms019-3-10-su55-h0bh - Round of 32
23 - adelaide - 2023-2843-ms023-3-9-ke29-cg04 - Round of 32
24 - adelaide - 2023-2843-ms022-3-8-d0co-kf17 - Round of 32
25 - adelaide - 2023-2843-ms030-3-7-gc88-g628 - Round of 32
26 - adelaide - 2023-2843-ms017-3-6-hb64-tc61 - Round of 32
27 - adelaide - 2023-2843-ms021-3-5-ki95-o483 - Round of 32
28 - adelaide - 2023-2843-ms025-3-4-kd46-c0bc - Round of 32
29 - adelaide - 2023-2843-ms026-3-3-k0ah-mc10 - Round of 32
30 - adelaide - 2023-2843-ms029-3-2-mk66-ge33 - Round of 32
31 - adelaide - 2023-2843-ms018-3-1-sx50-y268 - Round of 32
32 - adelaide - 2023-2843-qs004-2-4-kf17-da81 - 2nd Round Qualifying
33 - adelaide - 2023-2843-qs006-2-3-sx50-pd07 - 2nd Round Qualifying
34 - adelaide - 2023-2843-qs007-2-2-h0bh-d994 - 2nd Round Qualifying
35 - adelaide - 2023-2843-qs005-2-1-p09z-wb32 - 2nd Round Qualifying
36 - adelaide - 2023-2843-qs008-1-8-kf17-tb69 - 1st Round Qualifying
37 - adelaide - 2023-2843-qs010-1-7-wb32-hh26 - 1st Round Qualifying
38 - adelaide - 2023-2843-qs012-1-6-sx50-h997 - 1st Round Qualifying
39 - adelaide - 2023-2843-qs014-1-5-h0bh-bk24 - 1st Round Qualifying
40 - adelaide - 2023-2843-qs009-1-4-da81-w0c4 - 1st Round Qualifying
41 - adelaide - 2023-2843-qs015-1-3-d994-s0s1 - 1st Round Qualifying
42 - adelaide - 2023-2843-qs013-1-2-pd07-mh30 - 1st Round Qualifying
43 - adelaide - 2023-2843-qs011-1-1-p09z-z371 - 1st Round Qualifying

python3 match_stats.py  526.51s user 33.56s system 29% cpu 31:21.59 total
```
