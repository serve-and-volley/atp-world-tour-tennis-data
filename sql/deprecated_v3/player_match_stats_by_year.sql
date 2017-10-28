select
    match_year,
    player_id,
    player_slug,
    sum(matches) as total_matches,
    -- Serve stats
    --sum(service_points) as total_service_points,
    sum(aces) as total_aces,
    round(sum(aces)*1.0/sum(matches)*1.0, 2) as aces_per_match,
    round(sum(service_points)*1.0/sum(aces)*1.0, 2) as service_points_per_ace,
    sum(double_faults) as total_double_faults,
    round(sum(double_faults)*1.0/sum(matches)*1.0, 2) as double_faults_per_match,
    round(sum(service_points)*1.0/sum(double_faults)*1.0, 2) as service_points_per_double_fault,
    round(sum(aces)*1.0/sum(matches)*1.0, 2) - round(sum(double_faults)*1.0/sum(matches)*1.0, 2) as ace_dbl_fault_diff,

    round(sum(first_serve_points_won)*1.0/sum(first_serve_points_total)*1.0, 4) as first_serve_win_pct,
    round(sum(second_serve_points_won)*1.0/sum(second_serve_points_total)*1.0, 4) as second_serve_win_pct,
    round(sum(first_serve_return_won)*1.0/sum(first_serve_return_total)*1.0, 4) as first_serve_return_win_pct,
    round(sum(second_serve_return_won)*1.0/sum(second_serve_return_total)*1.0, 4) as second_serve_return_win_pct
    
from
    (
        (
            select
                match_year,
                winner_player_id as player_id,
                winner_slug as player_slug,
                count(winner_aces) as matches,
                sum(winner_aces) as aces,
                sum(winner_double_faults) as double_faults,
                sum(winner_service_points_total) as service_points,
                sum(winner_first_serve_points_won) as first_serve_points_won,
                sum(winner_first_serve_points_total) as first_serve_points_total,
                sum(winner_second_serve_points_won) as second_serve_points_won,
                sum(winner_second_serve_points_total) as second_serve_points_total,
                sum(winner_first_serve_return_won) as first_serve_return_won,
                sum(winner_first_serve_return_total) as first_serve_return_total,
                sum(winner_second_serve_return_won) as second_serve_return_won,
                sum(winner_second_serve_return_total) as second_serve_return_total

            from match_scores_stats

            where
                winner_slug = 'roger-federer' and
                --match_year = 2004 and
                winner_aces != 0 and
                winner_first_serve_return_won !=0

            group by
                match_year,
                player_id,
                player_slug
        )
        union
        (
            select
                match_year,
                loser_player_id as player_id,
                loser_slug as player_slug,
                count(loser_aces) as matches,
                sum(loser_aces) as aces,
                sum(loser_double_faults) as double_faults,
                sum(loser_service_points_total) as service_points,
                sum(loser_first_serve_points_won) as first_serve_points_won,
                sum(loser_first_serve_points_total) as first_serve_points_total,
                sum(loser_second_serve_points_won) as second_serve_points_won,
                sum(loser_second_serve_points_total) as second_serve_points_total,
                sum(loser_first_serve_return_won) as first_serve_return_won,
                sum(loser_first_serve_return_total) as first_serve_return_total,
                sum(loser_second_serve_return_won) as second_serve_return_won,
                sum(loser_second_serve_return_total) as second_serve_return_total

            from match_scores_stats

            where
                loser_slug = 'roger-federer' and
                --match_year = 2004 and
                loser_aces != 0 and
                loser_first_serve_return_won != 0

            group by
                match_year,
                player_id,
                player_slug
        )
        order by
            player_id
    ) as test

group by
    match_year,
    player_id,
    player_slug

order by
    match_year,
    --service_points_per_ace
    total_aces desc
    --second_serve_return_win_pct desc
