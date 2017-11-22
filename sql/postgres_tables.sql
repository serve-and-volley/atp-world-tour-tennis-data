/* * * * * * * * * * * * * * * * * * * * * * * * *
*                                                *
*   The following is for a PostgreSQL database   *   
*                                                *
* * * * * * * * * * * * * * * * * * * * * * * * */


/* TOURNAMENTS */
CREATE TABLE tournaments (
    id                              integer,
    tourney_year                    integer,
    tourney_order                   integer,
    tourney_name                    varchar(60),
    tourney_id                      integer,
    tourney_slug                    varchar(30),
    tourney_location                varchar(40),
    tourney_dates                   varchar(10),
    tourney_month                   integer,
    tourney_day                     integer,
    tourney_singles_draw            integer,
    tourney_doubles_draw            integer,
    tourney_conditions              varchar(10),
    tourney_surface                 varchar(10),
    tourney_fin_commit              varchar(15),
    tourney_url_suffix              varchar(200),
    singles_winner_name             varchar(40),
    singles_winner_url              varchar(200),
    singles_winner_player_slug      varchar(40),
    singles_winner_player_id        varchar(10),
    doubles_winner_1_name           varchar(40),
    doubles_winner_1_url            varchar(200),
    doubles_winner_1_player_slug    varchar(40),
    doubles_winner_1_player_id      varchar(10),
    doubles_winner_2_name           varchar(40),
    doubles_winner_2_url            varchar(200),
    doubles_winner_2_player_slug    varchar(40),
    doubles_winner_2_player_id      varchar(10),
    tourney_year_id                 varchar(15)
);

-- Ingesting the 'tournaments' indexed CSV file
\copy tournaments FROM '~/Desktop/test_atp/_output/1_tournaments/tournaments_indexed_1877-2016.csv' DELIMITER ',' CSV
\copy tournaments FROM '~/Documents/GitHub/atp-world-tour-tennis-data/python/tournaments_2017-2017_INDEXED.csv' DELIMITER ',' CSV
\copy tournaments FROM '~/Documents/GitHub/atp-world-tour-tennis-data/python/tournaments_2017_66-67.csv' DELIMITER ',' CSV

/* MATCH SCORES */
CREATE TABLE match_scores (
    id                      integer,
    tourney_year_id         varchar(15),
    tourney_order           integer,
    tourney_slug            varchar(30),
    tourney_url_suffix      varchar(200),
    tourney_round_name      varchar(20),
    round_order             integer,
    match_order             integer,
    winner_name             varchar(40),
    winner_player_id        varchar(10),
    winner_slug             varchar(40),
    loser_name              varchar(40),
    loser_player_id         varchar(10),
    loser_slug              varchar(40),
    winner_seed             varchar(5),
    loser_seed              varchar(5),
    match_score_tiebreaks   varchar(40),
    winner_sets_won         integer,
    loser_sets_won          integer,
    winner_games_won        integer,
    loser_games_won         integer,
    winner_tiebreaks_won    integer,
    loser_tiebreaks_won     integer,
    match_id                varchar(40),
    match_stats_url_suffix  varchar(200)
);

-- Ingesting the 'match_scores' indexed CSV file
\copy match_scores FROM '~/Desktop/test_atp/_output/2_match_scores/match_scores_indexed_1877-2016.csv' DELIMITER ',' CSV
\copy match_scores FROM '~/Documents/GitHub/atp-world-tour-tennis-data/python/match_scores_2017-2017_INDEXED.csv' DELIMITER ',' CSV
\copy match_scores FROM '~/Documents/GitHub/atp-world-tour-tennis-data/python/match_scores_2017_66-67_INDEXED.csv' DELIMITER ',' CSV

/* MATCH STATS */
CREATE TABLE match_stats (
    id                                  integer,
    tourney_order                       integer,
    match_id                            varchar(40),
    match_stats_url_suffix              varchar(200),
    match_time                          varchar(10),
    match_duration                      integer,
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
    winner_service_points_won           integer,
    winner_service_points_total         integer,
    winner_first_serve_return_won       integer,
    winner_first_serve_return_total     integer,
    winner_second_serve_return_won      integer,
    winner_second_serve_return_total    integer,
    winner_break_points_converted       integer,
    winner_break_points_return_total    integer,
    winner_service_games_played         integer,
    winner_return_games_played          integer,
    winner_return_points_won            integer,
    winner_return_points_total          integer,
    winner_total_points_won             integer,
    winner_total_points_total           integer,
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
    loser_service_points_won            integer,
    loser_service_points_total          integer,
    loser_first_serve_return_won        integer,
    loser_first_serve_return_total      integer,
    loser_second_serve_return_won       integer,
    loser_second_serve_return_total     integer,
    loser_break_points_converted        integer,
    loser_break_points_return_total     integer,
    loser_service_games_played          integer,
    loser_return_games_played           integer,
    loser_return_points_won             integer,
    loser_return_points_total           integer,
    loser_total_points_won              integer,
    loser_total_points_total            integer
);

-- Ingesting the 'match_stats' indexed CSV file
\copy match_stats FROM '~/Desktop/test_atp/_output/3_match_stats/match_stats_indexed_1991-2016.csv' DELIMITER ',' CSV
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/python/match_stats_2017_0-64_INDEXED.csv' DELIMITER ',' CSV
\copy match_stats FROM '~/Documents/GitHub/atp-world-tour-tennis-data/python/match_stats_2017_65-66_INDEXED.csv' DELIMITER ',' CSV

/* RANKINGS */
CREATE TABLE rankings (
    id                  integer,
    week_title          varchar(10),
    week_year           integer,
    week_month          integer,
    week_day            integer,
    rank_text           varchar(5),
    rank_number         integer,
    move_positions      integer,
    move_direction      varchar(5),
    player_age          integer,
    ranking_points      integer,
    tourneys_played     integer,
    player_url          varchar(100),
    player_slug         varchar(40),
    player_id           varchar(10)
);

-- Ingesting the 'rankings' indexed CSV file
\copy rankings FROM '~/Desktop/test_atp/rankings_1973-2016_INDEXED.csv' DELIMITER ',' CSV
\copy rankings FROM '~/Documents/GitHub/atp-world-tour-tennis-data/python/rankings_2017_0-37_INDEXED.csv' DELIMITER ',' CSV

/* PLAYERS */
CREATE TABLE players (
    id              integer,
    player_id       varchar(10),
    player_slug     varchar(40),
    first_name      varchar(40),
    last_name       varchar(40),
    player_url      varchar(200),
    flag_code       varchar(10),
    residence       varchar(60),
    birthplace      varchar(60),
    birthdate       varchar(15),
    birth_year      integer,
    birth_month     integer,
    birth_day       integer,
    turned_pro      integer,
    weight_lbs      integer,
    weight_kg       integer,
    height_ft       integer,
    height_inches   integer,
    height_cm       integer,
    handedness      varchar(15),
    backhand        varchar(20)
);

\copy players FROM '~/Documents/GitHub/atp-world-tour-tennis-data/python/player_overviews_INDEXED.csv' DELIMITER ',' CSV