select
    losses.player_id,
    losses.player_name,
    count(match_year) as simpsons_wins,
    losses.simpsons_losses,
    round(count(match_year)*1.0/(count(match_year) + losses.simpsons_losses)*1.0, 2) as win_loss_pct
from
    (
    select
        loser_player_id as player_id,
        loser_name as player_name,
        count(match_year) as simpsons_losses
    from match_scores_stats
    where
        match_year >= 1991
        and loser_total_points_won > winner_total_points_won
    group by
        loser_player_id,
        loser_name
    order by
        count(match_year) desc
    ) as losses
left join match_scores_stats
on match_scores_stats.winner_player_id = losses.player_id
where
    match_year >= 1991
    and loser_total_points_won > winner_total_points_won
group by
    losses.player_id,
    losses.player_name,
    losses.simpsons_losses
order by 
    losses.simpsons_losses desc
    --win_loss_pct
