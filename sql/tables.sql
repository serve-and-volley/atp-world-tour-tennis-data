/* TOURNAMENTS */
CREATE TABLE tournaments (
    tourney_year_id                 varchar,
    tourney_order                   integer,
    tourney_type                    varchar,
    tourney_name                    varchar,
    tourney_id                      integer,
    tourney_slug                    varchar,
    tourney_location                varchar,
    tourney_date                    varchar,
    tourney_year                    integer,
    tourney_month                   integer,
    tourney_day                     integer,
    tourney_singles_draw            integer,
    tourney_doubles_draw            integer,
    tourney_conditions              varchar,
    tourney_surface                 varchar,
    tourney_fin_commit_raw          varchar,
    currency                        varchar,
    tourney_fin_commit              integer,
    tourney_url_suffix              varchar,
    singles_winner_name             varchar,
    singles_winner_url              varchar,
    singles_winner_player_slug      varchar,
    singles_winner_player_id        varchar,
    doubles_winner_1_name           varchar,
    doubles_winner_1_url            varchar,
    doubles_winner_1_player_slug    varchar,
    doubles_winner_1_player_id      varchar,
    doubles_winner_2_name           varchar,
    doubles_winner_2_url            varchar,
    doubles_winner_2_player_slug    varchar,
    doubles_winner_2_player_id      varchar
);

\copy tournaments FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/1_tournaments/tournaments_1877-1967.csv' DELIMITER ',' CSV;
\copy tournaments FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/1_tournaments/tournaments_1968-1969.csv' DELIMITER ',' CSV;
\copy tournaments FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/1_tournaments/tournaments_1970-1979.csv' DELIMITER ',' CSV;
\copy tournaments FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/1_tournaments/tournaments_1980-1989.csv' DELIMITER ',' CSV;
\copy tournaments FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/1_tournaments/tournaments_1990-1999.csv' DELIMITER ',' CSV;
\copy tournaments FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/1_tournaments/tournaments_2000-2009.csv' DELIMITER ',' CSV;
\copy tournaments FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/1_tournaments/tournaments_2010-2019.csv' DELIMITER ',' CSV;
\copy tournaments FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/1_tournaments/tournaments_2020-2022.csv' DELIMITER ',' CSV;


/* MATCH SCORES */
CREATE TABLE match_scores (
    tourney_year_id         varchar,
    tourney_order           integer,
    tourney_name            varchar,
    tourney_slug            varchar,
    tourney_url_suffix      varchar,
    start_date              varchar,
    start_year              integer,
    start_month             integer,
    start_day               integer,
    end_date                varchar,
    end_year                integer,
    end_month               integer,
    end_day                 integer,
    currency                varchar,
    prize_money             integer,
    match_index             varchar,
    tourney_round_name      varchar,
    round_order             integer,
    match_order             integer,
    winner_name             varchar,
    winner_player_id        varchar,
    winner_slug             varchar,
    loser_name              varchar,
    loser_player_id         varchar,
    loser_slug              varchar,
    winner_seed             varchar,
    loser_seed              varchar,
    match_score_tiebreaks   varchar,
    winner_sets_won         integer,
    loser_sets_won          integer,
    winner_games_won        integer,
    loser_games_won         integer,
    winner_tiebreaks_won    integer,
    loser_tiebreaks_won     integer,
    match_id                varchar,
    match_stats_url_suffix  varchar
);

\copy match_scores FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/2_match_scores/match_scores_1877-1967.csv' DELIMITER ',' CSV;
\copy match_scores FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/2_match_scores/match_scores_1968-1969.csv' DELIMITER ',' CSV;
\copy match_scores FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/2_match_scores/match_scores_1970-1979.csv' DELIMITER ',' CSV;
\copy match_scores FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/2_match_scores/match_scores_1980-1989.csv' DELIMITER ',' CSV;
\copy match_scores FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/2_match_scores/match_scores_1990-1999.csv' DELIMITER ',' CSV;
\copy match_scores FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/2_match_scores/match_scores_2000-2009.csv' DELIMITER ',' CSV;
\copy match_scores FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/2_match_scores/match_scores_2010-2019.csv' DELIMITER ',' CSV;
\copy match_scores FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/2_match_scores/match_scores_2020-2022.csv' DELIMITER ',' CSV;


/* MATCH STATS */
CREATE TABLE match_stats (
    match_id                            varchar,
    tourney_slug                        varchar,
    match_stats_url_suffix              varchar,
    match_time                          varchar,
    match_duration                      integer,
    winner_slug                         varchar,
    winner_serve_rating                 integer,
    winner_aces                         integer,
    winner_double_faults                integer,
    winner_first_serves_in              integer,
    winner_first_serves_total           integer,
    winner_first_serve_points_won       integer,
    winner_first_serve_points_total     integer,
    winner_second_serve_points_won      integer,
    winner_second_serve_points_total    integer,
    winner_break_points_saved           integer,
    winner_break_points_serve_total     integer,
    winner_service_games_played         integer,
    winner_return_rating                integer,
    winner_first_serve_return_won       integer,
    winner_first_serve_return_total     integer,
    winner_second_serve_return_won      integer,
    winner_second_serve_return_total    integer,
    winner_break_points_converted       integer,
    winner_break_points_return_total    integer,
    winner_return_games_played          integer,
    winner_service_points_won           integer,
    winner_service_points_total         integer,
    winner_return_points_won            integer,
    winner_return_points_total          integer,
    winner_total_points_won             integer,
    winner_total_points_total           integer,
    loser_slug                          varchar,
    loser_serve_rating                  integer,
    loser_aces                          integer,
    loser_double_faults                 integer,
    loser_first_serves_in               integer,
    loser_first_serves_total            integer,
    loser_first_serve_points_won        integer,
    loser_first_serve_points_total      integer,
    loser_second_serve_points_won       integer,
    loser_second_serve_points_total     integer,
    loser_break_points_saved            integer,
    loser_break_points_serve_total      integer,
    loser_service_games_played          integer,
    loser_return_rating                 integer,
    loser_first_serve_return_won        integer,
    loser_first_serve_return_total      integer,
    loser_second_serve_return_won       integer,
    loser_second_serve_return_total     integer,
    loser_break_points_converted        integer,
    loser_break_points_return_total     integer,
    loser_return_games_played           integer,
    loser_service_points_won            integer,
    loser_service_points_total          integer,
    loser_return_points_won             integer,
    loser_return_points_total           integer,
    loser_total_points_won              integer,
    loser_total_points_total            integer
);

\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_1991.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_1992.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_1993.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_1994.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_1995.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_1996.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_1997.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_1998.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_1999.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2000.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2001.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2002.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2003.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2004.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2005.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2006.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2007.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2008.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2009.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2010.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2011.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2012.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2013.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2014.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2015.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2016.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2017.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2018.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2019.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2020.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2021.csv' DELIMITER ',' CSV;
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/csv/3_match_stats/match_stats_2022.csv' DELIMITER ',' CSV;

