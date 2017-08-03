select
    tournaments.singles_winner_name as player_name,
    tournaments.singles_winner_player_id as player_id,
    count(tournaments.singles_winner_player_id) as total,
    foo_clay.grass as grass,
    foo_clay.clay as clay,
    foo_clay.hard as hard,
    foo_clay.carpet as carpet
from
    (
    select
        tournaments.singles_winner_name as player_name,
        tournaments.singles_winner_player_id as player_id,  
        foo_hard.grass as grass,
        foo_hard.hard as hard,
        foo_hard.carpet as carpet,
        count(tournaments.singles_winner_player_id) as clay
    from
        (
        select
            tournaments.singles_winner_name as player_name,
            tournaments.singles_winner_player_id as player_id,
            foo_grass.grass as grass,
            foo_grass.carpet as carpet,
            count(tournaments.singles_winner_player_id) as hard
        from
            (
            select
                tournaments.singles_winner_name as player_name,
                tournaments.singles_winner_player_id as player_id,
                foo_carpet.carpet as carpet,
                count(tournaments.singles_winner_player_id) as grass
            from
                (
                select
                    singles_winner_name as player_name,
                    singles_winner_player_id as player_id,
                    count(singles_winner_player_id) as carpet
                from tournaments
                    where
                        singles_winner_player_id is not null and
                        tourney_surface = 'Carpet'
                group by
                    singles_winner_name,
                    singles_winner_player_id
                order by count(singles_winner_player_id) desc
                ) as foo_carpet
            right join tournaments
            on foo_carpet.player_id = tournaments.singles_winner_player_id
            where
                singles_winner_player_id is not null and
                tourney_surface = 'Grass'
            group by
                tournaments.singles_winner_name,
                tournaments.singles_winner_player_id,
                foo_carpet.carpet
            order by count(tournaments.singles_winner_player_id) desc
            ) as foo_grass
        right join tournaments
        on foo_grass.player_id = tournaments.singles_winner_player_id
        where
            singles_winner_player_id is not null and
            tourney_surface = 'Hard'
        group by
            tournaments.singles_winner_name,
            tournaments.singles_winner_player_id,
            foo_grass.grass,
            foo_grass.carpet
        order by count(tournaments.singles_winner_player_id) desc
        ) as foo_hard
    right join tournaments
    on foo_hard.player_id = tournaments.singles_winner_player_id
    where
        singles_winner_player_id is not null and
        tourney_surface = 'Clay'
    group by
        tournaments.singles_winner_name,
        tournaments.singles_winner_player_id,
        foo_hard.grass,
        foo_hard.hard,
        foo_hard.carpet
    order by count(tournaments.singles_winner_player_id) desc
    ) as foo_clay
right join tournaments
on foo_clay.player_id = tournaments.singles_winner_player_id
where
    singles_winner_player_id is not null
group by
    tournaments.singles_winner_name,
    tournaments.singles_winner_player_id,   
    foo_clay.grass,
    foo_clay.clay,
    foo_clay.hard,
    foo_clay.carpet 
order by count(tournaments.singles_winner_player_id) desc
