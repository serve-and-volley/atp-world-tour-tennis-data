from bs4 import BeautifulSoup

def match_data(html, winner_id, loser_id):
    
    soup = BeautifulSoup(html, 'html.parser')
    # Match duration
    match_time = soup.find('td', 'time').text.strip()
    match_duration = 60 * int(match_time.split(':')[0]) + int(match_time.split(':')[1])

    # Player id's and slugs
    right_a = soup.find('div', 'team team2')
    if right_a is None:
        return 'MISSING DATA'
    else:
        right_href = right_a.find('a').get('href')
        right_slug = right_href.split('/')[5]
        right_player_id = right_href.split('/')[6].lower()

        left_a = soup.find('div', 'team team1')
        left_href = left_a.find('a').get('href')
        left_slug = left_href.split('/')[5]
        left_player_id = left_href.split('/')[6].lower()

        # right stats
        right_div = soup.find_all('div', 'p2Stats')

        # left stats
        left_div = soup.find_all('div', 'p1Stats')

        # Match winner and loser player IDs
        if winner_id == right_player_id:
            winner_array = []
            for div in right_div:
                winner_array.append(div)
            loser_array = []
            for div in left_div:
                loser_array.append(div)
        if winner_id == left_player_id:
            winner_array = []
            for div in left_div:
                winner_array.append(div)
            loser_array = []
            for div in right_div:
                loser_array.append(div)

        winner_player_id = winner_id
        loser_player_id = loser_id

        # Winner stats
        winner_serve_rating = int(winner_array[0].find('a').text)
        winner_aces = int(winner_array[2].find('span').text.strip())
        winner_double_faults = int(winner_array[4].find('span').text.strip())

        winner_first_serve = winner_array[6].find('span').text.strip().split(' ')[0].split('/')
        winner_first_serves_in = int(winner_first_serve[0])
        winner_first_serves_total = int(winner_first_serve[1])

        winner_first_serve_points = winner_array[8].find('span').text.strip().split(' ')[0].split('/')
        winner_first_serve_points_won = int(winner_first_serve_points[0])
        winner_first_serve_points_total = int(winner_first_serve_points[1])

        winner_second_serve_points = winner_array[10].find('span').text.strip().split(' ')[0].split('/')
        winner_second_serve_points_won = int(winner_second_serve_points[0])
        winner_second_serve_points_total = int(winner_second_serve_points[1])

        winner_break_points = winner_array[12].find('span').text.strip().split(' ')[0].split('/')
        winner_break_points_saved = int(winner_break_points[0])
        winner_break_points_serve_total = int(winner_break_points[1])

        winner_service_games_played = int(winner_array[14].find('span').text.strip())

        winner_return_rating = int(winner_array[16].find('a').text)

        winner_first_serve_return = winner_array[18].find('span').text.strip().split(' ')[0].split('/')
        winner_first_serve_return_won = int(winner_first_serve_return[0])
        winner_first_serve_return_total = int(winner_first_serve_return[1])

        winner_second_serve_return = winner_array[20].find('span').text.strip().split(' ')[0].split('/')
        winner_second_serve_return_won = int(winner_second_serve_return[0])
        winner_second_serve_return_total = int(winner_second_serve_return[1])

        winner_break_points = winner_array[22].find('span').text.strip().split(' ')[0].split('/')
        winner_break_points_converted = int(winner_break_points[0])
        winner_break_points_return_total = int(winner_break_points[1])

        winner_return_games_played = int(winner_array[24].find('span').text.strip())

        winner_service_points = winner_array[26].find('span').text.strip().split(' ')[0].split('/')
        winner_service_points_won = int(winner_service_points[0])
        winner_service_points_total = int(winner_service_points[1])

        winner_return_points = winner_array[28].find('span').text.strip().split(' ')[0].split('/')
        winner_return_points_won = int(winner_return_points[0])
        winner_return_points_total = int(winner_return_points[1])

        winner_total_points = winner_array[30].find('span').text.strip().split(' ')[0].split('/')
        winner_total_points_won = int(winner_total_points[0])
        winner_total_points_total = int(winner_total_points[1])

        # Loser stats
        loser_serve_rating = int(loser_array[0].find('a').text)
        loser_aces = int(loser_array[2].find('span').text.strip())
        loser_double_faults = int(loser_array[4].find('span').text.strip())

        loser_first_serve = loser_array[6].find('span').text.strip().split(' ')[0].split('/')
        loser_first_serves_in = int(loser_first_serve[0])
        loser_first_serves_total = int(loser_first_serve[1])

        loser_first_serve_points = loser_array[8].find('span').text.strip().split(' ')[0].split('/')
        loser_first_serve_points_won = int(loser_first_serve_points[0])
        loser_first_serve_points_total = int(loser_first_serve_points[1])

        loser_second_serve_points = loser_array[10].find('span').text.strip().split(' ')[0].split('/')
        loser_second_serve_points_won = int(loser_second_serve_points[0])
        loser_second_serve_points_total = int(loser_second_serve_points[1])

        loser_break_points = loser_array[12].find('span').text.strip().split(' ')[0].split('/')
        loser_break_points_saved = int(loser_break_points[0])
        loser_break_points_serve_total = int(loser_break_points[1])

        loser_service_games_played = int(loser_array[14].find('span').text.strip())

        loser_return_rating = int(loser_array[16].find('a').text)

        loser_first_serve_return = loser_array[18].find('span').text.strip().split(' ')[0].split('/')
        loser_first_serve_return_won = int(loser_first_serve_return[0])
        loser_first_serve_return_total = int(loser_first_serve_return[1])

        loser_second_serve_return = loser_array[20].find('span').text.strip().split(' ')[0].split('/')
        loser_second_serve_return_won = int(loser_second_serve_return[0])
        loser_second_serve_return_total = int(loser_second_serve_return[1])

        loser_break_points = loser_array[22].find('span').text.strip().split(' ')[0].split('/')
        loser_break_points_converted = int(loser_break_points[0])
        loser_break_points_return_total = int(loser_break_points[1])

        loser_return_games_played = int(loser_array[24].find('span').text.strip())

        loser_service_points = loser_array[26].find('span').text.strip().split(' ')[0].split('/')
        loser_service_points_won = int(loser_service_points[0])
        loser_service_points_total = int(loser_service_points[1])

        loser_return_points = loser_array[28].find('span').text.strip().split(' ')[0].split('/')
        loser_return_points_won = int(loser_return_points[0])
        loser_return_points_total = int(loser_return_points[1])

        loser_total_points = loser_array[30].find('span').text.strip().split(' ')[0].split('/')
        loser_total_points_won = int(loser_total_points[0])
        loser_total_points_total = int(loser_total_points[1])

        match_data = [match_time, match_duration]
        winner_data = [winner_player_id, winner_serve_rating, winner_aces, winner_double_faults, winner_first_serves_in, winner_first_serves_total, winner_first_serve_points_won, winner_first_serve_points_total, winner_second_serve_points_won, winner_second_serve_points_total, winner_break_points_saved, winner_break_points_serve_total, winner_service_games_played, winner_return_rating, winner_first_serve_return_won, winner_first_serve_return_total, winner_second_serve_return_won, winner_second_serve_return_total, winner_break_points_converted, winner_break_points_return_total, winner_return_games_played, winner_service_points_won, winner_service_points_total, winner_return_points_won, winner_return_points_total, winner_total_points_won, winner_total_points_total]
        loser_data = [loser_player_id, loser_serve_rating, loser_aces, loser_double_faults, loser_first_serves_in, loser_first_serves_total, loser_first_serve_points_won, loser_first_serve_points_total, loser_second_serve_points_won, loser_second_serve_points_total, loser_break_points_saved, loser_break_points_serve_total, loser_service_games_played, loser_return_rating, loser_first_serve_return_won, loser_first_serve_return_total, loser_second_serve_return_won, loser_second_serve_return_total, loser_break_points_converted, loser_break_points_return_total, loser_return_games_played, loser_service_points_won, loser_service_points_total, loser_return_points_won, loser_return_points_total, loser_total_points_won, loser_total_points_total]

        scraped_data = match_data + winner_data + loser_data

        return scraped_data