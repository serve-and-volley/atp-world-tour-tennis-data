# ATP World Tour tennis data

This repository contains Python scripts that scrape tennis data from the <a href="http://www.atpworldtour.com/" target="_blank">ATP World Tour</a> website, as of Dec 2016. 
<br />
(Note: If the site does a redesign, then these scripts will no longer work.)

## Example
The following Python script: 

* <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/python/atp_match_data_player.py" target="_blank">atp_match_data_player.py</a>

collects all of the tournament and match stats for a single player in a given year, and exports the following example CSV file:

* <a href="https://github.com/serve-and-volley/atp-world-tour-tennis-data/blob/master/csv/roger-federer_2015.csv" target="_blank">roger-federer_2015.csv</a> (33 KB)

The columns headers in the CSV file are the following:
```
tourney_year
tourney_name
tourney_name_slug
tourney_id
tourney_location
tourney_dates
tourney_singles_draw
tourney_doubles_draw
tourney_conditions
tourney_surface
player_name
player_slug
player_id
player_event_points
player_ranking
match_round
opponent_name
opponent_name_slug
opponent_player_id
opponent_rank
match_win_loss
match_score
sets_won
sets_lost
sets_total
games_won
games_lost
games_total
tiebreaks_won
tiebreaks_lost
tiebreaks_total
match_time
match_duration
player_aces
player_double_faults
player_first_serves_in
player_first_serves_total
player_first_serve_percentage
player_first_serve_points_won
player_first_serve_points_total
player_first_serve_points_won_percentage
player_second_serve_points_won
player_second_serve_points_total
player_second_serve_points_won_percentage
player_break_points_saved
player_break_points_serve_total
player_break_points_saved_percentage
player_service_points_won
player_service_points_total
player_service_points_won_percentage
player_first_serve_return_won
player_first_serve_return_total
player_first_serve_return_percentage
player_second_serve_return_won
player_second_serve_return_total
player_second_serve_return_won_percentage
player_break_points_converted
player_break_points_return_total
player_break_points_converted_percentage
player_service_games_played
player_return_games_played
player_return_points_won
player_return_points_total
player_total_points_won
player_total_points_total
player_total_points_won_percentage
opponent_aces
opponent_double_faults
opponent_first_serves_in
opponent_first_serves_total
opponent_first_serve_percentage
opponent_first_serve_points_won
opponent_first_serve_points_total
opponent_first_serve_points_won_percentage
opponent_second_serve_points_won
opponent_second_serve_points_total
opponent_second_serve_points_won_percentage
opponent_break_points_saved
opponent_break_points_serve_total
opponent_break_points_saved_percentage
opponent_service_points_won
opponent_service_points_total
opponent_service_points_won_percentage
opponent_first_serve_return_won
opponent_first_serve_return_total
opponent_first_serve_return_percentage
opponent_second_serve_return_won
opponent_second_serve_return_total
opponent_second_serve_return_won_percentage
opponent_break_points_converted
opponent_break_points_return_total
opponent_break_points_converted_percentage
opponent_service_games_played
opponent_return_games_played
opponent_return_points_won
opponent_return_points_total
opponent_total_points_won
opponent_total_points_total
opponent_total_points_won_percentage
```

The Python script takes input arguments from the command line, so for this example it would be:
```
$ time python atp_match_data_player.py "http://www.atpworldtour.com/players/roger-federer/f324/player-activity?year=2016"
```

In addition to the CSV output, the console output is the following, for debugging purposes, since the ATP website is not coded properly, and there are often scraping errors, upon which I would have to revise the XPaths and/or the code accordingly. This console output allows me to figure out exactly which match the scraper broke down.

```
$ time python atp_match_data_player.py "http://www.atpworldtour.com/players/roger-federer/f324/player-activity?year=2016"
Barclays ATP World Tour Finals | Finals | Novak Djokovic
Barclays ATP World Tour Finals | Semi-Finals | Stan Wawrinka
Barclays ATP World Tour Finals | Round Robin | Kei Nishikori
Barclays ATP World Tour Finals | Round Robin | Novak Djokovic
Barclays ATP World Tour Finals | Round Robin | Tomas Berdych
ATP World Tour Masters 1000 Paris | Round of 16 | John Isner
ATP World Tour Masters 1000 Paris | Round of 32 | Andreas Seppi
Basel | Finals | Rafael Nadal
Basel | Semi-Finals | Jack Sock
Basel | Quarter-Finals | David Goffin
Basel | Round of 16 | Philipp Kohlschreiber
Basel | Round of 32 | Mikhail Kukushkin
ATP World Tour Masters 1000 Shanghai | Round of 32 | Albert Ramos-Vinolas
SUI vs. NED WG Play-Off | Round Robin | Thiemo de Bakker
SUI vs. NED WG Play-Off | Round Robin | Jesse Huta Galung
US Open | Finals | Novak Djokovic
US Open | Semi-Finals | Stan Wawrinka
US Open | Quarter-Finals | Richard Gasquet
US Open | Round of 16 | John Isner
US Open | Round of 32 | Philipp Kohlschreiber
US Open | Round of 64 | Steve Darcis
US Open | Round of 128 | Leonardo Mayer
ATP World Tour Masters 1000 Cincinnati | Finals | Novak Djokovic
ATP World Tour Masters 1000 Cincinnati | Semi-Finals | Andy Murray
ATP World Tour Masters 1000 Cincinnati | Quarter-Finals | Feliciano Lopez
ATP World Tour Masters 1000 Cincinnati | Round of 16 | Kevin Anderson
ATP World Tour Masters 1000 Cincinnati | Round of 32 | Roberto Bautista Agut
Wimbledon | Finals | Novak Djokovic
Wimbledon | Semi-Finals | Andy Murray
Wimbledon | Quarter-Finals | Gilles Simon
Wimbledon | Round of 16 | Roberto Bautista Agut
Wimbledon | Round of 32 | Sam Groth
Wimbledon | Round of 64 | Sam Querrey
Wimbledon | Round of 128 | Damir Dzumhur
Halle | Finals | Andreas Seppi
Halle | Semi-Finals | Ivo Karlovic
Halle | Quarter-Finals | Florian Mayer
Halle | Round of 16 | Ernests Gulbis
Halle | Round of 32 | Philipp Kohlschreiber
Roland Garros | Quarter-Finals | Stan Wawrinka
Roland Garros | Round of 16 | Gael Monfils
Roland Garros | Round of 32 | Damir Dzumhur
Roland Garros | Round of 64 | Marcel Granollers
Roland Garros | Round of 128 | Alejandro Falla
ATP World Tour Masters 1000 Rome | Finals | Novak Djokovic
ATP World Tour Masters 1000 Rome | Semi-Finals | Stan Wawrinka
ATP World Tour Masters 1000 Rome | Quarter-Finals | Tomas Berdych
ATP World Tour Masters 1000 Rome | Round of 16 | Kevin Anderson
ATP World Tour Masters 1000 Rome | Round of 32 | Pablo Cuevas
ATP World Tour Masters 1000 Madrid | Round of 32 | Nick Kyrgios
Istanbul | Finals | Pablo Cuevas
Istanbul | Semi-Finals | Diego Schwartzman
Istanbul | Quarter-Finals | Daniel Gimeno-Traver
Istanbul | Round of 16 | Jarkko Nieminen
ATP World Tour Masters 1000 Monte Carlo | Round of 16 | Gael Monfils
ATP World Tour Masters 1000 Monte Carlo | Round of 32 | Jeremy Chardy
ATP World Tour Masters 1000 Indian Wells | Finals | Novak Djokovic
ATP World Tour Masters 1000 Indian Wells | Semi-Finals | Milos Raonic
ATP World Tour Masters 1000 Indian Wells | Quarter-Finals | Tomas Berdych
ATP World Tour Masters 1000 Indian Wells | Round of 16 | Jack Sock
ATP World Tour Masters 1000 Indian Wells | Round of 32 | Andreas Seppi
ATP World Tour Masters 1000 Indian Wells | Round of 64 | Diego Schwartzman
Dubai | Finals | Novak Djokovic
Dubai | Semi-Finals | Borna Coric
Dubai | Quarter-Finals | Richard Gasquet
Dubai | Round of 16 | Fernando Verdasco
Dubai | Round of 32 | Mikhail Youzhny
Australian Open | Round of 32 | Andreas Seppi
Australian Open | Round of 64 | Simone Bolelli
Australian Open | Round of 128 | Yen-Hsun Lu
Brisbane | Finals | Milos Raonic
Brisbane | Semi-Finals | Grigor Dimitrov
Brisbane | Quarter-Finals | James Duckworth
Brisbane | Round of 16 | John Millman

real	15m59.516s
user	0m19.618s
sys	0m1.259s
```
