from scraping import *

def tourney_matches(tourney_year, tourney_index):
    url_prefix = "https://www.atptour.com"
    year_url = "https://www.atptour.com/en/scores/results-archive?year=" + tourney_year
    year_tree = html_parse_tree(year_url)

    # Tourney URL suffixes
    tourney_details_url_xpath = "//tr[contains(@class, 'tourney-result')][*]/td[8]/a/@href"
    tourney_url_suffixes = xpath_parse(year_tree, tourney_details_url_xpath)

    # Tourney names
    tourney_name_xpath = "//tr[contains(@class, 'tourney-result')]/td[3]/a/text()"
    tourney_name_parsed = xpath_parse(year_tree, tourney_name_xpath)
    tourney_names = regex_strip_array(tourney_name_parsed)

    # Tourney date
    tourney_date_xpath = "//tr[contains(@class, 'tourney-result')]/td[3]/span[contains(@class, 'tourney-dates')]/text()"
    tourney_date_parsed = xpath_parse(year_tree, tourney_date_xpath)
    tourney_dates = regex_strip_array(tourney_date_parsed)

    # Tourney info
    tourney_name = tourney_names[tourney_index]
    tourney_date = tourney_dates[tourney_index]
    tourney_slug = tourney_url_suffixes[tourney_index].split('/')[4]
    tourney_id = tourney_url_suffixes[tourney_index].split('/')[5]
    tourney_url = url_prefix + tourney_url_suffixes[tourney_index]
    tourney_tree = html_parse_tree(tourney_url)

    # Tourney round count
    tourney_round_name_xpath = "//table[contains(@class, 'day-table')]/thead/tr/th/text()"
    tourney_round_name_parsed = xpath_parse(tourney_tree, tourney_round_name_xpath)
    tourney_round_count = len(tourney_round_name_parsed)

    matches = []
    # Iterate through each round
    match_counter = 1
    for j in range(0, tourney_round_count):

        # Round order and match count
        round_order = j + 1
        tourney_round_name = tourney_round_name_parsed[j]
        round_match_count_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j + 1) + "]/tr/td[contains(@class, 'day-table-name')][1]/a/text()"
        round_match_count_parsed = xpath_parse(tourney_tree, round_match_count_xpath)
        round_match_count = len(round_match_count_parsed)

        # Iterate through each match
        for k in range(0, round_match_count):

            # Match order and round match ID
            match_order = k + 1
            round_match_id = str(tourney_round_count - j) + '-' + str(round_match_count - k)

            # Winner info
            winner_name_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j + 1) + "]/tr[" + str(k + 1) + "]/td[contains(@class, 'day-table-name')][1]/a/text()"
            winner_name_parsed = xpath_parse(tourney_tree, winner_name_xpath)
            winner_url_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j + 1) + "]/tr[" + str(k + 1) + "]/td[contains(@class, 'day-table-name')][1]/a/@href"
            winner_url_parsed = xpath_parse(tourney_tree, winner_url_xpath)
            winner_name = winner_name_parsed[0]
            winner_url = winner_url_parsed[0]
            winner_url_split = winner_url.split('/')
            winner_slug = winner_url_split[3]
            winner_player_id = winner_url_split[4]  

            # Loser info
            loser_name_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j + 1) + "]/tr[" + str(k + 1) + "]/td[contains(@class, 'day-table-name')][2]/a/text()"
            loser_name_parsed = xpath_parse(tourney_tree, loser_name_xpath)
            loser_url_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j +1) + "]/tr[" + str(k + 1) + "]/td[contains(@class, 'day-table-name')][2]/a/@href"
            loser_url_parsed = xpath_parse(tourney_tree, loser_url_xpath)

            try:                
                loser_name = loser_name_parsed[0]
                loser_url = loser_url_parsed[0]
                loser_url
                loser_url_split = loser_url.split('/')
                loser_slug = loser_url_split[3]
                loser_player_id = loser_url_split[4]
            except Exception:
                loser_name = ''
                loser_url = ''
                loser_slug = ''
                loser_player_id = ''

            # Match stats URL
            match_stats_url_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j + 1) + "]/tr[" + str(k + 1) + "]/td[contains(@class, 'day-table-score')]/a/@href"
            match_stats_url_parsed = xpath_parse(tourney_tree, match_stats_url_xpath)
            if len(match_stats_url_parsed) > 0:
                match_stats_url_suffix = match_stats_url_parsed[0]
                match_year = match_stats_url_suffix.split('/')[3]
                match_index = match_stats_url_suffix.split('/')[7]
                match_id = tourney_year + "-" + tourney_id + "-" + match_index + "-" + round_match_id + "-" + winner_player_id + "-" + loser_player_id
                match_info = [match_counter, tourney_slug, match_id, round_match_id, tourney_round_name, winner_player_id, loser_player_id, match_stats_url_suffix]
                matches.append(match_info)
                match_counter += 1
    return matches


