select
    tournaments.tourney_year as tourney_year,
    count(tournaments.tourney_name) as grass,
    foo_clay.clay as clay,
    foo_clay.hard as hard,
    foo_clay.carpet as carpet
from
    (
    select
        tournaments.tourney_year as tourney_year,
        count(tournaments.tourney_name) as clay,
        foo_hard.hard as hard,
        foo_hard.carpet as carpet
    from
        (
        select
            tournaments.tourney_year as tourney_year,
            foo_carpet.carpet as carpet,
            count(tournaments.tourney_name) as hard
        from
            (
            select
                tourney_year,
                count(tourney_name) as carpet
            from tournaments
            where 
                tourney_surface = 'Carpet' and
                tourney_year >= 1968
            group by
                tourney_year,
                tourney_surface
            order by
                tourney_year
            ) as foo_carpet
        right join tournaments
        on tournaments.tourney_year = foo_carpet.tourney_year
        where
            tournaments.tourney_year >= 1968 and
            tournaments.tourney_surface = 'Hard'
        group by 
            tournaments.tourney_year,
            foo_carpet.carpet
        order by
            tournaments.tourney_year
        ) as foo_hard
    right join tournaments
    on tournaments.tourney_year = foo_hard.tourney_year
    where
        tournaments.tourney_year >= 1968 and
        tournaments.tourney_surface = 'Clay'
    group by 
        tournaments.tourney_year,
        foo_hard.carpet,
        foo_hard.hard
    order by
        tournaments.tourney_year
    ) as foo_clay
right join tournaments
on tournaments.tourney_year = foo_clay.tourney_year
where
    tournaments.tourney_year >= 1968 and
    tournaments.tourney_surface = 'Grass'
group by 
    tournaments.tourney_year,
    foo_clay.clay,
    foo_clay.hard,
    foo_clay.carpet
order by
    tournaments.tourney_year
