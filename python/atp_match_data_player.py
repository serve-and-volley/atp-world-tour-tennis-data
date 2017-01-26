# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                                       #
#   This script scrapes the ATP match data and stats by player name and by year                         #
#                                                                                                       #
#   Example of how to run this script on the command line:                                              #
#   $ python atp_match_data_player.py roger-federer f324 1998 2000                                      #
#                                                                                                       #
#   Where the command line arguments are the following:                                                 #
#                                                                                                       #
#   - "roger-federer": this is the "player slug",                                                       #
#     and is determined by an example player year activity URL like the following:                      #
#     http://www.atpworldtour.com/players/roger-federer/f324/player-activity?year=1998                  #
#                                                                                                       #
#   - "f324": this is the "player id",                                                                  #
#     and is also determined by an example player year activity URL                                     #
#                                                                                                       #
#   Note:   This script can only scrape the verstion of the ATP website as of Dec 23, 2016.             #
#           If the site layout is redesigned, then all of the XPaths in this script becomes invalid.    #
#                                                                                                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from lxml import html
import requests
import re
import json
import csv
import sys

def html_parse(url, xpath):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    result = tree.xpath(xpath)
    return result

def regex_strip_string(string):
    string = re.sub('\n', '', string)
    string = re.sub('\r', '', string)
    string = re.sub('\t', '', string)
    return string

def regex_strip_array(array):
    for i in xrange(0, len(array)):
        array[i] = regex_strip_string(array[i])
    return array

# Parsing the command line input
player_slug = sys.argv[1]
player_id = sys.argv[2]
start_year = int(sys.argv[3])
end_year = int(sys.argv[4])

# Player name
player_slug_split = player_slug.split("-")
new_name_array = []
for name in player_slug_split:
    name_list = list(name)
    new_partial_name = ""
    for i in xrange(0, len(name_list)):
        if i == 0:
            new_partial_name += name_list[i].capitalize()
        else:
            new_partial_name += name_list[i]
    new_name_array.append(new_partial_name)
player_name = " ".join(new_name_array)

# Setup
url_prefix = "http://www.atpworldtour.com"
csv_array = []
header = [['tourney_year', 'tourney_name', 'tourney_name_slug', 'tourney_id', 'tourney_location', 'tourney_dates', 'tourney_singles_draw', 'tourney_doubles_draw', 'tourney_conditions', 'tourney_surface', 'player_name', 'player_slug', 'player_id', 'player_event_points', 'player_ranking', 'match_round', 'opponent_name', 'opponent_name_slug', 'opponent_player_id', 'opponent_rank', 'match_win_loss', 'match_score', 'sets_won', 'sets_lost', 'sets_total', 'games_won', 'games_lost', 'games_total', 'tiebreaks_won', 'tiebreaks_lost', 'tiebreaks_total', 'match_time', 'match_duration', 'player_aces', 'player_double_faults', 'player_first_serves_in', 'player_first_serves_total', 'player_first_serve_points_won', 'player_first_serve_points_total', 'player_second_serve_points_won', 'player_second_serve_points_total', 'player_break_points_saved', 'player_break_points_serve_total', 'player_service_points_won', 'player_service_points_total', 'player_first_serve_return_won', 'player_first_serve_return_total', 'player_second_serve_return_won', 'player_second_serve_return_total', 'player_break_points_converted', 'player_break_points_return_total', 'player_service_games_played', 'player_return_games_played', 'player_return_points_won', 'player_return_points_total', 'player_total_points_won', 'player_total_points_total', 'opponent_aces', 'opponent_double_faults', 'opponent_first_serves_in', 'opponent_first_serves_total', 'opponent_first_serve_points_won', 'opponent_first_serve_points_total', 'opponent_second_serve_points_won', 'opponent_second_serve_points_total', 'opponent_break_points_saved', 'opponent_break_points_serve_total', 'opponent_service_points_won', 'opponent_service_points_total', 'opponent_first_serve_return_won', 'opponent_first_serve_return_total', 'opponent_second_serve_return_won', 'opponent_second_serve_return_total', 'opponent_break_points_converted', 'opponent_break_points_return_total', 'opponent_service_games_played', 'opponent_return_games_played', 'opponent_return_points_won', 'opponent_return_points_total', 'opponent_total_points_won', 'opponent_total_points_total']]
csv_array = header + csv_array

# Iterate through each year
for h in xrange(start_year, end_year + 1):
    year_url = url_prefix + "/players/" + player_slug + "/" + player_id + "/player-activity?year=" + str(h)
    tourney_year = h

    # XPaths
    tourney_count_xpath = "//div[contains(@class, 'activity-tournament-table')]"
    tourney_count_parsed = html_parse(year_url, tourney_count_xpath)
    tourney_count = len(tourney_count_parsed)

    tourney_location_xpath = "//span[contains(@class, 'tourney-location')]/text()"
    tourney_location_parsed = html_parse(year_url, tourney_location_xpath)
    tourney_location_cleaned = regex_strip_array(tourney_location_parsed)

    tourney_dates_xpath = "//span[contains(@class, 'tourney-dates')]/text()"
    tourney_dates_parsed = html_parse(year_url, tourney_dates_xpath)
    tourney_dates_cleaned = regex_strip_array(tourney_dates_parsed)

    tourney_draw_xpath = "//a[contains(@class, 'not-in-system')]/span/text()"
    tourney_draw_parsed = html_parse(year_url, tourney_draw_xpath)
    tourney_draw_cleaned = regex_strip_array(tourney_draw_parsed)

    tourney_conditions_xpath = "//div[contains(., 'Outdoor') or contains(., 'Indoor')]/text()[normalize-space()]"
    tourney_conditions_parsed = html_parse(year_url, tourney_conditions_xpath)

    tourney_surface_xpath = "//div[contains(., 'Outdoor') or contains(., 'Indoor')]/span/text()[normalize-space()]"
    tourney_surface_parsed = html_parse(year_url, tourney_surface_xpath)

    #tourney_prize_money_xpath = "//td[contains(@class, 'prize-money')]/div/div/span/text()"
    #tourney_prize_money_parsed = html_parse(year_url, tourney_prize_money_xpath)
    #tourney_prize_money_cleaned = regex_strip_array(tourney_prize_money_parsed)

    #tourney_fin_commit_xpath = "//td[contains(@class, 'fin-commit')]/div/div/span/text()"
    #tourney_fin_commit_parsed = html_parse(year_url, tourney_fin_commit_xpath)
    #tourney_fin_commit_cleaned = regex_strip_array(tourney_fin_commit_parsed)

    player_tourney_activity_xpath = "//div[contains(@class, 'activity-tournament-caption')]/text()"
    player_tourney_activity_parsed = html_parse(year_url, player_tourney_activity_xpath)

    # Debug
    #print str(tourney_year) + " | " + str(tourney_count)

    # Iterate over each tournament
    for i in xrange(0, tourney_count):

        tourney_href_xpath = "//div[contains(@class, 'activity-tournament-table')][" + str(i+1) + "]/table[1]/tbody/tr/td[2]/a/@href"
        tourney_href_parsed = html_parse(year_url, tourney_href_xpath)

        # Condition for Davis Cup tournaments, which lack info that the other tournaments have
        if len(tourney_href_parsed) == 0:
            tourney_name_slug = ""
            tourney_id = ""
            tourney_name_xpath = "//div[contains(@class, 'activity-tournament-table')][" + str(i+1) + "]/table[1]/tbody/tr/td[2]/span[contains(@class, 'tourney-title')]/text()"
            tourney_name_parsed = html_parse(year_url, tourney_name_xpath)
            tourney_name_cleaned = regex_strip_array(tourney_name_parsed)
            tourney_name = tourney_name_cleaned[0]
        # Condition for non-Davis Cup tournaments
        else:
            tourney_href = tourney_href_parsed[0]
            tourney_href_split = tourney_href.split("/")
            tourney_name_slug = tourney_href_split[3]    
            tourney_id = tourney_href_split[4]
            tourney_name_xpath = "//div[contains(@class, 'activity-tournament-table')][" + str(i+1) + "]/table[1]/tbody/tr/td[2]/a/text()"
            tourney_name_parsed = html_parse(year_url, tourney_name_xpath)
            tourney_name = tourney_name_parsed[0]        

        tourney_location = tourney_location_cleaned[i]
        tourney_dates = tourney_dates_cleaned[i]
        tourney_singles_draw = tourney_draw_cleaned[2*i]
        tourney_doubles_draw = tourney_draw_cleaned[2*i + 1]

        tourney_conditions = tourney_conditions_parsed[i].strip()
        tourney_surface = tourney_surface_parsed[i].strip()

        # Unicode problem
        # tourney_prize_money = tourney_prize_money_cleaned[i]
        # tourney_fin_commit = tourney_fin_commit_cleaned[i]
        #tourney_prize_money = ""
        #tourney_fin_commit = ""

        player_tourney_activity_split = player_tourney_activity_parsed[i].split(", ")
        player_event_points = player_tourney_activity_split[0].split(": ")[1]
        player_ranking = player_tourney_activity_split[1].split(": ")[1]

        # Unicode problem
        # player_prize_money = player_tourney_activity_split[2].split(": ")[1]
        #player_prize_money = ""

        mega_table_xpath = "//table[contains(@class, 'mega-table')][" + str(i+1) + "]/tbody/tr"
        mega_table_parsed = html_parse(year_url,mega_table_xpath)
        tourney_match_count = len(mega_table_parsed)

        # Iterate over each match
        for j in xrange(0, tourney_match_count):

            # Mega table XPaths
            match_round_xpath = "//table[contains(@class, 'mega-table')][" + str(i+1) + "]/tbody/tr[" + str(j+1) + "]/td[1]/text()"
            match_round_parsed = html_parse(year_url, match_round_xpath)

            opponent_name_xpath = "//table[contains(@class, 'mega-table')][" + str(i+1) + "]/tbody/tr[" + str(j+1) + "]/td[3]/div[2]/a/text()"
            opponent_name_parsed = html_parse(year_url, opponent_name_xpath)

            opponent_player_url_xpath = "//table[contains(@class, 'mega-table')][" + str(i+1) + "]/tbody/tr[" + str(j+1) + "]/td[3]/div[2]/a/@href"
            opponent_player_url_parsed = html_parse(year_url, opponent_player_url_xpath)

            opponent_rank_xpath = "//table[contains(@class, 'mega-table')][" + str(i+1) + "]/tbody/tr[" + str(j+1) + "]/td[2]/text()"
            opponent_rank_parsed = html_parse(year_url, opponent_rank_xpath)

            match_won_loss_xpath = "//table[contains(@class, 'mega-table')][" + str(i+1) + "]/tbody/tr[" + str(j+1) + "]/td[4]/text()"
            match_won_loss_parsed = html_parse(year_url, match_won_loss_xpath)

            match_score_node_xpath = "//table[contains(@class, 'mega-table')][" + str(i+1) + "]/tbody/tr[" + str(j+1) + "]/td[5]/a/node()"
            match_score_node_parsed = html_parse(year_url, match_score_node_xpath)

            match_score_text_xpath = "//table[contains(@class, 'mega-table')][" + str(i+1) + "]/tbody/tr[" + str(j+1) + "]/td[5]/a/text()"
            match_score_text_parsed = html_parse(year_url, match_score_text_xpath)       

            match_score_tiebreak_xpath = "//table[contains(@class, 'mega-table')][" + str(i+1) + "]/tbody/tr[" + str(j+1) + "]/td[5]/a/sup/text()"
            match_score_tiebreak_parsed = html_parse(year_url, match_score_tiebreak_xpath)

            match_stats_url_xpath = "//table[contains(@class, 'mega-table')][" + str(i+1) + "]/tbody/tr[" + str(j+1) + "]/td[5]/a/@href"
            match_stats_url_parsed = html_parse(year_url, match_stats_url_xpath)

            # Condition to skip "Bye" matches
            if len(opponent_name_parsed) > 0:
                match_round = match_round_parsed[0]
                opponent_name = opponent_name_parsed[0]
                opponent_player_url_split = opponent_player_url_parsed[0].split("/")
                opponent_name_slug = opponent_player_url_split[3]
                opponent_player_id = opponent_player_url_split[4]
                opponent_rank = regex_strip_string(opponent_rank_parsed[0])
                match_win_loss = regex_strip_string(match_won_loss_parsed[0])

                # Condition if match has no tiebreaks
                if len(match_score_tiebreak_parsed) == 0:

                    # Match score
                    match_score = match_score_node_parsed[0].strip()
                    
                    # Count games won/lost
                    match_score_split = match_score.split(" ")
                    games_won = 0
                    games_lost = 0
                    for k in xrange(0, len(match_score_split)):                    
                        # Regex match to test for numbers, to skip cases like '(RET)'
                        test = re.match(r'\d*', match_score_split[k])
                        # Condition when set score is two single digit numbers, e.g. 64
                        if len(test.group(0)) > 0:
                            if len(test.group(0)) == 2:
                                games_won += int(match_score_split[k][0])
                                games_lost += int(match_score_split[k][1])
                            # Condition when set score has a dash, e.g. "8-10"
                            else: 
                                games_won += int(match_score_split[k].split("-")[0])
                                games_lost += int(match_score_split[k].split("-")[1])

                    games_total = games_won + games_lost

                    # Count tiebreaks
                    tiebreaks_won = ""
                    tiebreaks_lost = ""
                    tiebreaks_total = ""

                    # Count sets
                    sets_total = len(match_score_split)
                    sets_won = 0
                    sets_lost = 0
                    for k in xrange(0, sets_total):
                        # Regex match to test for numbers, to skip cases like '(RET)'
                        test = re.match(r'\d*', match_score_split[k])
                        # DEBUG
                        # print tourney_name + " | " + match_round + " | " + opponent_name + " | " + str(len(test.group(0)))
                        # Condition when set score is two single digit numbers, e.g. 64
                        if len(test.group(0)) > 0:
                            if len(test.group(0)) == 2:
                                if int(match_score_split[k][0]) > int(match_score_split[k][1]):
                                    sets_won += 1
                                else:
                                    sets_lost += 1
                            # Condition when set score has a dash, "e.g. 8-10"
                            else:
                                if (int(match_score_split[k].split("-")[0] > match_score_split[k].split("-")[1])):
                                    sets_won += 1
                                else:
                                    sets_lost += 1
                
                # Condition if match score has tiebreaks
                else:
                    
                    # Match score       
                    match_score = ""
                    tiebreak_set_split_count = len(match_score_text_parsed)
                    for k in xrange(0, tiebreak_set_split_count):
                        if k < tiebreak_set_split_count - 1:
                            match_score_text_parsed[k] = match_score_text_parsed[k].strip()
                            match_score += match_score_text_parsed[k]
                            match_score += "(" + match_score_tiebreak_parsed[k] + ") "
                        if k == tiebreak_set_split_count - 1:
                            match_score_text_parsed[k] = match_score_text_parsed[k].strip()
                            match_score += match_score_text_parsed[k]

                    # Count games won/lost
                    match_score_no_tiebreak_text = ""
                    for k in xrange(0, len(match_score_text_parsed)):
                        match_score_no_tiebreak_text += " " + match_score_text_parsed[k].strip()                    
                    match_score_no_tiebreak_text = match_score_no_tiebreak_text.strip()
                    match_score_no_tiebreak_array = match_score_no_tiebreak_text.split(" ")
                    games_won = 0
                    games_lost = 0
                    for k in xrange(0, len(match_score_no_tiebreak_array)):
                        # Regex match to test for numbers, to skip cases like '(RET)'
                        test = re.match(r'\d*', match_score_no_tiebreak_array[k])
                        if len(test.group(0)) == 2:
                            games_won += int(match_score_no_tiebreak_array[k][0])
                            games_lost += int(match_score_no_tiebreak_array[k][1])
                    games_total = games_won + games_lost

                    # Count tiebreaks
                    tiebreaks_total = len(match_score_tiebreak_parsed)
                    tiebreaks_won = 0
                    tiebreaks_lost = 0
                    for k in xrange(0, len(match_score_no_tiebreak_array)):
                        if match_score_no_tiebreak_array[k] == "76":
                            tiebreaks_won += 1
                        if match_score_no_tiebreak_array[k] == "67":
                            tiebreaks_lost += 1

                    # Count sets
                    sets_total = len(match_score_no_tiebreak_array)
                    sets_won = 0
                    sets_lost = 0
                    for k in xrange(0, sets_total):
                        # Regex match to test for numbers, to skip cases like '(RET)'
                        test = re.match(r'\d*', match_score_no_tiebreak_array[k])
                        if len(test.group(0)) == 2:
                            if int(match_score_no_tiebreak_array[k][0]) > int(match_score_no_tiebreak_array[k][1]):
                                sets_won += 1
                            else:
                                sets_lost += 1

                # Parsing the individual match stats from the JSON data
                # Condition if the match stats URL is unavailable
                if len(match_stats_url_parsed[0]) == 0:
                    match_time = ""
                    match_duration = ""

                    player_aces = ""
                    player_double_faults = ""
                    player_first_serves_in = ""
                    player_first_serves_total = ""
                    #player_first_serve_percentage = ""
                    player_first_serve_points_won = ""
                    player_first_serve_points_total = ""
                    #player_first_serve_points_won_percentage = ""
                    player_second_serve_points_won = ""
                    player_second_serve_points_total = ""
                    #player_second_serve_points_won_percentage = ""
                    player_break_points_saved = ""
                    player_break_points_serve_total = ""
                    #player_break_points_saved_percentage = ""
                    player_service_points_won = ""
                    player_service_points_total = ""
                    #player_service_points_won_percentage = ""
                    player_first_serve_return_won = ""
                    player_first_serve_return_total = ""
                    #player_first_serve_return_percentage = ""
                    player_second_serve_return_won = ""
                    player_second_serve_return_total = ""
                    #player_second_serve_return_won_percentage = ""
                    player_break_points_converted = ""
                    player_break_points_return_total = ""
                    #player_break_points_converted_percentage = ""
                    player_service_games_played = ""
                    player_return_games_played = ""
                    #player_service_games_played_percentage = ""
                    #player_return_games_played_percentage = ""
                    player_return_points_won = ""
                    player_return_points_total = ""
                    player_total_points_won = ""
                    player_total_points_total = ""
                    #player_total_points_won_percentage = ""

                    opponent_aces = ""
                    opponent_double_faults = ""
                    opponent_first_serves_in = ""
                    opponent_first_serves_total = ""
                    #opponent_first_serve_percentage = ""
                    opponent_first_serve_points_won = ""
                    opponent_first_serve_points_total = ""
                    #opponent_first_serve_points_won_percentage = ""
                    opponent_second_serve_points_won = ""
                    opponent_second_serve_points_total = ""
                    #opponent_second_serve_points_won_percentage = ""
                    opponent_break_points_saved = ""
                    opponent_break_points_serve_total = ""
                    #opponent_break_points_saved_percentage = ""
                    opponent_service_points_won = ""
                    opponent_service_points_total = ""
                    #opponent_service_points_won_percentage = ""
                    opponent_first_serve_return_won = ""
                    opponent_first_serve_return_total = ""
                    #opponent_first_serve_return_percentage = ""
                    opponent_second_serve_return_won = ""
                    opponent_second_serve_return_total = ""
                    #opponent_second_serve_return_won_percentage = ""
                    opponent_break_points_converted = ""
                    opponent_break_points_return_total = ""
                    #opponent_break_points_converted_percentage = ""
                    opponent_service_games_played = ""
                    opponent_return_games_played = ""
                    #opponent_service_games_played_percentage = ""
                    #opponent_return_games_played_percentage = ""
                    opponent_return_points_won = ""
                    opponent_return_points_total = ""
                    opponent_total_points_won = ""
                    opponent_total_points_total = ""
                    #opponent_total_points_won_percentage = ""                

                # Condition if the match stats URL is available
                elif len(match_stats_url_parsed[0]) > 0:
                    match_stats_url = url_prefix + match_stats_url_parsed[0]

                    match_time_xpath = "//td[contains(@class, 'time')]/text()"
                    match_time_parsed = html_parse(match_stats_url, match_time_xpath)
                    match_time_cleaned = regex_strip_array(match_time_parsed)
                    
                    # match_time = match_time_cleaned[0].split(": ")[1]
                    try:
                        match_time = match_time_cleaned[0].replace("Time: ", "")
                        match_time_split = match_time.split(":")            
                        match_time_hours = int(match_time_split[0])
                        match_time_minutes = int(match_time_split[1])
                        match_duration = 60*match_time_hours + match_time_minutes                                        
                    except Exception:
                        match_time = ""
                        match_duration = ""

                    match_stats_xpath = "//*[@id='matchStatsData']/text()"
                    match_stats_parsed = html_parse(match_stats_url, match_stats_xpath)

                    match_stats_cleaned = regex_strip_string(match_stats_parsed[0])
                    json_string = match_stats_cleaned
                    json_data = json.loads(json_string)

                    # Winner stats
                    winner_aces = json_data[0]["playerStats"]["Aces"]
                    winner_double_faults = json_data[0]["playerStats"]["DoubleFaults"]

                    winner_first_serves_in = json_data[0]["playerStats"]["FirstServeDividend"]
                    winner_first_serves_total = json_data[0]["playerStats"]["FirstServeDivisor"]
                    #winner_first_serve_percentage = json_data[0]["playerStats"]["FirstServePercentage"]

                    winner_first_serve_points_won = json_data[0]["playerStats"]["FirstServePointsWonDividend"]
                    winner_first_serve_points_total = json_data[0]["playerStats"]["FirstServePointsWonDivisor"]
                    #winner_first_serve_points_won_percentage = json_data[0]["playerStats"]["FirstServePointsWonPercentage"]

                    winner_second_serve_points_won = json_data[0]["playerStats"]["SecondServePointsWonDividend"]
                    winner_second_serve_points_total = json_data[0]["playerStats"]["SecondServePointsWonDivisor"]
                    #winner_second_serve_points_won_percentage = json_data[0]["playerStats"]["SecondServePointsWonPercentage"]

                    winner_break_points_saved = json_data[0]["playerStats"]["BreakPointsSavedDividend"]
                    winner_break_points_serve_total = json_data[0]["playerStats"]["BreakPointsSavedDivisor"]
                    #winner_break_points_saved_percentage = json_data[0]["playerStats"]["BreakPointsSavedPercentage"]

                    winner_service_points_won = json_data[0]["playerStats"]["TotalServicePointsWonDividend"]
                    winner_service_points_total = json_data[0]["playerStats"]["TotalServicePointsWonDivisor"]
                    #winner_service_points_won_percentage = json_data[0]["playerStats"]["TotalServicePointsWonPercentage"]

                    winner_first_serve_return_won = json_data[0]["playerStats"]["FirstServeReturnPointsDividend"]
                    winner_first_serve_return_total = json_data[0]["playerStats"]["FirstServeReturnPointsDivisor"]
                    #winner_first_serve_return_percentage = json_data[0]["playerStats"]["FirstServeReturnPointsPercentage"]

                    winner_second_serve_return_won = json_data[0]["playerStats"]["SecondServePointsDividend"]
                    winner_second_serve_return_total = json_data[0]["playerStats"]["SecondServePointsDivisor"]
                    #winner_second_serve_return_won_percentage = json_data[0]["playerStats"]["SecondServePointsPercentage"]

                    winner_break_points_converted = json_data[0]["playerStats"]["BreakPointsConvertedDividend"]
                    winner_break_points_return_total = json_data[0]["playerStats"]["BreakPointsConvertedDivisor"]
                    #winner_break_points_converted_percentage = json_data[0]["playerStats"]["BreakPointsConvertedPercentage"]

                    winner_service_games_played = json_data[0]["playerStats"]["ServiceGamesPlayed"]
                    winner_return_games_played = json_data[0]["playerStats"]["ReturnGamesPlayed"]
                    #winner_service_games_played_percentage = json_data[0]["playerStats"]["ServiceGamesPlayedPercentage"]
                    #winner_return_games_played_percentage = json_data[0]["playerStats"]["ReturnGamesPlayedPercentage"]

                    winner_return_points_won = json_data[0]["playerStats"]["TotalReturnPointsWonDividend"]
                    winner_return_points_total = json_data[0]["playerStats"]["TotalReturnPointsWonDivisor"]

                    winner_total_points_won = json_data[0]["playerStats"]["TotalPointsWonDividend"]
                    winner_total_points_total = json_data[0]["playerStats"]["TotalPointsWonDivisor"]            
                    #winner_total_points_won_percentage = json_data[0]["playerStats"]["TotalPointsWonPercentage"]

                    # Loser stats
                    loser_aces = json_data[0]["opponentStats"]["Aces"]
                    loser_double_faults = json_data[0]["opponentStats"]["DoubleFaults"]

                    loser_first_serves_in = json_data[0]["opponentStats"]["FirstServeDividend"]
                    loser_first_serves_total = json_data[0]["opponentStats"]["FirstServeDivisor"]
                    #loser_first_serve_percentage = json_data[0]["opponentStats"]["FirstServePercentage"]

                    loser_first_serve_points_won = json_data[0]["opponentStats"]["FirstServePointsWonDividend"]
                    loser_first_serve_points_total = json_data[0]["opponentStats"]["FirstServePointsWonDivisor"]
                    #loser_first_serve_points_won_percentage = json_data[0]["opponentStats"]["FirstServePointsWonPercentage"]

                    loser_second_serve_points_won = json_data[0]["opponentStats"]["SecondServePointsWonDividend"]
                    loser_second_serve_points_total = json_data[0]["opponentStats"]["SecondServePointsWonDivisor"]
                    #loser_second_serve_points_won_percentage = json_data[0]["opponentStats"]["SecondServePointsWonPercentage"]

                    loser_break_points_saved = json_data[0]["opponentStats"]["BreakPointsSavedDividend"]
                    loser_break_points_serve_total = json_data[0]["opponentStats"]["BreakPointsSavedDivisor"]
                    #loser_break_points_saved_percentage = json_data[0]["opponentStats"]["BreakPointsSavedPercentage"]

                    loser_service_points_won = json_data[0]["opponentStats"]["TotalServicePointsWonDividend"]
                    loser_service_points_total = json_data[0]["opponentStats"]["TotalServicePointsWonDivisor"]
                    #loser_service_points_won_percentage = json_data[0]["opponentStats"]["TotalServicePointsWonPercentage"]

                    loser_first_serve_return_won = json_data[0]["opponentStats"]["FirstServeReturnPointsDividend"]
                    loser_first_serve_return_total = json_data[0]["opponentStats"]["FirstServeReturnPointsDivisor"]
                    #loser_first_serve_return_percentage = json_data[0]["opponentStats"]["FirstServeReturnPointsPercentage"]

                    loser_second_serve_return_won = json_data[0]["opponentStats"]["SecondServePointsDividend"]
                    loser_second_serve_return_total = json_data[0]["opponentStats"]["SecondServePointsDivisor"]
                    #loser_second_serve_return_won_percentage = json_data[0]["opponentStats"]["SecondServePointsPercentage"]

                    loser_break_points_converted = json_data[0]["opponentStats"]["BreakPointsConvertedDividend"]
                    loser_break_points_return_total = json_data[0]["opponentStats"]["BreakPointsConvertedDivisor"]
                    #loser_break_points_converted_percentage = json_data[0]["opponentStats"]["BreakPointsConvertedPercentage"]

                    loser_service_games_played = json_data[0]["opponentStats"]["ServiceGamesPlayed"]
                    loser_return_games_played = json_data[0]["opponentStats"]["ReturnGamesPlayed"]
                    #loser_service_games_played_percentage = json_data[0]["opponentStats"]["ServiceGamesPlayedPercentage"]
                    #loser_return_games_played_percentage = json_data[0]["opponentStats"]["ReturnGamesPlayedPercentage"]

                    loser_return_points_won = json_data[0]["opponentStats"]["TotalReturnPointsWonDividend"]
                    loser_return_points_total = json_data[0]["opponentStats"]["TotalReturnPointsWonDivisor"]

                    loser_total_points_won = json_data[0]["opponentStats"]["TotalPointsWonDividend"]
                    loser_total_points_total = json_data[0]["opponentStats"]["TotalPointsWonDivisor"]           
                    #loser_total_points_won_percentage = json_data[0]["opponentStats"]["TotalPointsWonPercentage"]

                    if match_win_loss == "W":
                        player_aces = winner_aces
                        player_double_faults = winner_double_faults
                        player_first_serves_in = winner_first_serves_in
                        player_first_serves_total = winner_first_serves_total
                        #player_first_serve_percentage = winner_first_serve_percentage
                        player_first_serve_points_won = winner_first_serve_points_won
                        player_first_serve_points_total = winner_first_serve_points_total
                        #player_first_serve_points_won_percentage = winner_first_serve_points_won_percentage
                        player_second_serve_points_won = winner_second_serve_points_won
                        player_second_serve_points_total = winner_second_serve_points_total
                        #player_second_serve_points_won_percentage = winner_second_serve_points_won_percentage
                        player_break_points_saved = winner_break_points_saved
                        player_break_points_serve_total = winner_break_points_serve_total
                        #player_break_points_saved_percentage = winner_break_points_saved_percentage
                        player_service_points_won = winner_service_points_won
                        player_service_points_total = winner_service_points_total
                        #player_service_points_won_percentage = winner_service_points_won_percentage
                        player_first_serve_return_won = winner_first_serve_return_won
                        player_first_serve_return_total = winner_first_serve_return_total
                        #player_first_serve_return_percentage = winner_first_serve_return_percentage
                        player_second_serve_return_won = winner_second_serve_return_won
                        player_second_serve_return_total = winner_second_serve_return_total
                        #player_second_serve_return_won_percentage = winner_second_serve_return_won_percentage
                        player_break_points_converted = winner_break_points_converted
                        player_break_points_return_total = winner_break_points_return_total
                        #player_break_points_converted_percentage = winner_break_points_converted_percentage
                        player_service_games_played = winner_service_games_played
                        player_return_games_played = winner_return_games_played
                        #player_service_games_played_percentage = winner_service_games_played_percentage
                        #player_return_games_played_percentage = winner_return_games_played_percentage
                        player_return_points_won = winner_return_points_won
                        player_return_points_total = winner_return_points_total
                        player_total_points_won = winner_total_points_won
                        player_total_points_total = winner_total_points_total
                        #player_total_points_won_percentage = winner_total_points_won_percentage

                        opponent_aces = loser_aces
                        opponent_double_faults = loser_double_faults
                        opponent_first_serves_in = loser_first_serves_in
                        opponent_first_serves_total = loser_first_serves_total
                        #opponent_first_serve_percentage = loser_first_serve_percentage
                        opponent_first_serve_points_won = loser_first_serve_points_won
                        opponent_first_serve_points_total = loser_first_serve_points_total
                        #opponent_first_serve_points_won_percentage = loser_first_serve_points_won_percentage
                        opponent_second_serve_points_won = loser_second_serve_points_won
                        opponent_second_serve_points_total = loser_second_serve_points_total
                        #opponent_second_serve_points_won_percentage = loser_second_serve_points_won_percentage
                        opponent_break_points_saved = loser_break_points_saved
                        opponent_break_points_serve_total = loser_break_points_serve_total
                        #opponent_break_points_saved_percentage = loser_break_points_saved_percentage
                        opponent_service_points_won = loser_service_points_won
                        opponent_service_points_total = loser_service_points_total
                        #opponent_service_points_won_percentage = loser_service_points_won_percentage
                        opponent_first_serve_return_won = loser_first_serve_return_won
                        opponent_first_serve_return_total = loser_first_serve_return_total
                        #opponent_first_serve_return_percentage = loser_first_serve_return_percentage
                        opponent_second_serve_return_won = loser_second_serve_return_won
                        opponent_second_serve_return_total = loser_second_serve_return_total
                        #opponent_second_serve_return_won_percentage = loser_second_serve_return_won_percentage
                        opponent_break_points_converted = loser_break_points_converted
                        opponent_break_points_return_total = loser_break_points_return_total
                        #opponent_break_points_converted_percentage = loser_break_points_converted_percentage
                        opponent_service_games_played = loser_service_games_played
                        opponent_return_games_played = loser_return_games_played
                        #opponent_service_games_played_percentage = loser_service_games_played_percentage
                        #opponent_return_games_played_percentage = loser_return_games_played_percentage
                        opponent_return_points_won = loser_return_points_won
                        opponent_return_points_total = loser_return_points_total
                        opponent_total_points_won = loser_total_points_won
                        opponent_total_points_total = loser_total_points_total
                        #opponent_total_points_won_percentage = loser_total_points_won_percentage

                    elif match_win_loss == "L":
                        player_aces = loser_aces
                        player_double_faults = loser_double_faults
                        player_first_serves_in = loser_first_serves_in
                        player_first_serves_total = loser_first_serves_total
                        #player_first_serve_percentage = loser_first_serve_percentage
                        player_first_serve_points_won = loser_first_serve_points_won
                        player_first_serve_points_total = loser_first_serve_points_total
                        #player_first_serve_points_won_percentage = loser_first_serve_points_won_percentage
                        player_second_serve_points_won = loser_second_serve_points_won
                        player_second_serve_points_total = loser_second_serve_points_total
                        #player_second_serve_points_won_percentage = loser_second_serve_points_won_percentage
                        player_break_points_saved = loser_break_points_saved
                        player_break_points_serve_total = loser_break_points_serve_total
                        #player_break_points_saved_percentage = loser_break_points_saved_percentage
                        player_service_points_won = loser_service_points_won
                        player_service_points_total = loser_service_points_total
                        #player_service_points_won_percentage = loser_service_points_won_percentage
                        player_first_serve_return_won = loser_first_serve_return_won
                        player_first_serve_return_total = loser_first_serve_return_total
                        #player_first_serve_return_percentage = loser_first_serve_return_percentage
                        player_second_serve_return_won = loser_second_serve_return_won
                        player_second_serve_return_total = loser_second_serve_return_total
                        #player_second_serve_return_won_percentage = loser_second_serve_return_won_percentage
                        player_break_points_converted = loser_break_points_converted
                        player_break_points_return_total = loser_break_points_return_total
                        #player_break_points_converted_percentage = loser_break_points_converted_percentage
                        player_service_games_played = loser_service_games_played
                        player_return_games_played = loser_return_games_played
                        #player_service_games_played_percentage = loser_service_games_played_percentage
                        #player_return_games_played_percentage = loser_return_games_played_percentage
                        player_return_points_won = loser_return_points_won
                        player_return_points_total = loser_return_points_total
                        player_total_points_won = loser_total_points_won
                        player_total_points_total = loser_total_points_total
                        #player_total_points_won_percentage = loser_total_points_won_percentage

                        opponent_aces = winner_aces
                        opponent_double_faults = winner_double_faults
                        opponent_first_serves_in = winner_first_serves_in
                        opponent_first_serves_total = winner_first_serves_total
                        #opponent_first_serve_percentage = winner_first_serve_percentage
                        opponent_first_serve_points_won = winner_first_serve_points_won
                        opponent_first_serve_points_total = winner_first_serve_points_total
                        #opponent_first_serve_points_won_percentage = winner_first_serve_points_won_percentage
                        opponent_second_serve_points_won = winner_second_serve_points_won
                        opponent_second_serve_points_total = winner_second_serve_points_total
                        #opponent_second_serve_points_won_percentage = winner_second_serve_points_won_percentage
                        opponent_break_points_saved = winner_break_points_saved
                        opponent_break_points_serve_total = winner_break_points_serve_total
                        #opponent_break_points_saved_percentage = winner_break_points_saved_percentage
                        opponent_service_points_won = winner_service_points_won
                        opponent_service_points_total = winner_service_points_total
                        #opponent_service_points_won_percentage = winner_service_points_won_percentage
                        opponent_first_serve_return_won = winner_first_serve_return_won
                        opponent_first_serve_return_total = winner_first_serve_return_total
                        #opponent_first_serve_return_percentage = winner_first_serve_return_percentage
                        opponent_second_serve_return_won = winner_second_serve_return_won
                        opponent_second_serve_return_total = winner_second_serve_return_total
                        #opponent_second_serve_return_won_percentage = winner_second_serve_return_won_percentage
                        opponent_break_points_converted = winner_break_points_converted
                        opponent_break_points_return_total = winner_break_points_return_total
                        #opponent_break_points_converted_percentage = winner_break_points_converted_percentage
                        opponent_service_games_played = winner_service_games_played
                        opponent_return_games_played = winner_return_games_played
                        #opponent_service_games_played_percentage = winner_service_games_played_percentage
                        #opponent_return_games_played_percentage = winner_return_games_played_percentage
                        opponent_return_points_won = winner_return_points_won
                        opponent_return_points_total = winner_return_points_total
                        opponent_total_points_won = winner_total_points_won
                        opponent_total_points_total = winner_total_points_total
                        #opponent_total_points_won_percentage = winner_total_points_won_percentage



                # Command line output for debugging
                print str(tourney_year) + " | " + tourney_name + " | " + match_round + " | " + opponent_name
                
                # Store the data
                data = [tourney_year, tourney_name, tourney_name_slug, tourney_id, tourney_location, tourney_dates, tourney_singles_draw, tourney_doubles_draw, tourney_conditions, tourney_surface, player_name, player_slug, player_id, player_event_points, player_ranking, match_round, opponent_name, opponent_name_slug, opponent_player_id, opponent_rank, match_win_loss, match_score, sets_won, sets_lost, sets_total, games_won, games_lost, games_total, tiebreaks_won, tiebreaks_lost, tiebreaks_total, match_time, match_duration, player_aces, player_double_faults, player_first_serves_in, player_first_serves_total, player_first_serve_points_won, player_first_serve_points_total, player_second_serve_points_won, player_second_serve_points_total, player_break_points_saved, player_break_points_serve_total, player_service_points_won, player_service_points_total, player_first_serve_return_won, player_first_serve_return_total, player_second_serve_return_won, player_second_serve_return_total, player_break_points_converted, player_break_points_return_total, player_service_games_played, player_return_games_played, player_return_points_won, player_return_points_total, player_total_points_won, player_total_points_total, opponent_aces, opponent_double_faults, opponent_first_serves_in, opponent_first_serves_total, opponent_first_serve_points_won, opponent_first_serve_points_total, opponent_second_serve_points_won, opponent_second_serve_points_total, opponent_break_points_saved, opponent_break_points_serve_total, opponent_service_points_won, opponent_service_points_total, opponent_first_serve_return_won, opponent_first_serve_return_total, opponent_second_serve_return_won, opponent_second_serve_return_total, opponent_break_points_converted, opponent_break_points_return_total, opponent_service_games_played, opponent_return_games_played, opponent_return_points_won, opponent_return_points_total, opponent_total_points_won, opponent_total_points_total]
                csv_array.append(data)

                # Output to CSV file
                csv_out = open(player_slug + "_" + str(start_year) + "-" + str(end_year) + ".csv", 'wb')
                mywriter = csv.writer(csv_out)
                for row in csv_array:
                    mywriter.writerow(row)
                csv_out.close()
