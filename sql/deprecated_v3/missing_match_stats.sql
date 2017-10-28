select
    foo.match_year,
    count(match_scores_stats.match_year) as total_matches,
    foo.missing_stats,
    round(foo.missing_stats*1.0/count(match_scores_stats.match_year)*1.0, 4) as missing_pct
from
    (
    select
        match_year,
        count(match_year) as missing_stats
    from match_scores_stats
    where winner_aces is null or winner_second_serve_return_won = 0
    group by match_year
    order by match_year
    ) as foo

left join match_scores_stats
on match_scores_stats.match_year = foo.match_year

where
    foo.match_year >= 1991

group by
    foo.match_year,
    foo.missing_stats

order by foo.match_year
