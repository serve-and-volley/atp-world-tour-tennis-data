import sys
from lxml import html
import requests
import re
import csv
import time
import numbers

def array2csv(array, filename):
    with open(filename, "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter = ',')
        csvWriter.writerows(array)

def html_parse_tree(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree

def xpath_parse(tree, xpath):
    result = tree.xpath(xpath)
    return result

def regex_strip_array(array):
    for i in range(0, len(array)):
        array[i] = regex_strip_string(array[i]).strip()
    return array

def regex_strip_string(string):
    string = re.sub('\n', '', string).strip()
    string = re.sub('\r', '', string).strip()
    string = re.sub('\t', '', string).strip()
    return string

def format_spacing(max_spacing, variable):
    spacing_count = max_spacing - len(variable)
    output = ''
    for i in range(0, spacing_count):
        output += ' '
    return output

def fraction_stats(string):
    string = string.replace('(', '')
    string = string.replace(')', '')
    return string.split('/')

def scrape_match_stats(match_stats_url):
    match_tree = html_parse_tree(match_stats_url)

    # Match time
    try:
        match_time_xpath = "//td[contains(@class, 'time')]/text()"
        match_time_parsed = xpath_parse(match_tree, match_time_xpath)
        match_time_cleaned = regex_strip_array(match_time_parsed)
        match_time = match_time_cleaned[0].replace("Time: ", "")
        match_time_split = match_time.split(":")            
        match_time_hours = int(match_time_split[0])
        match_time_minutes = int(match_time_split[1])
        match_duration = 60*match_time_hours + match_time_minutes                                        
    except Exception:
        match_time = ""
        match_duration = ""

    # Match info
    match_year = match_stats_url_suffix.split('/')[3]
    tourney_id = match_stats_url_suffix.split('/')[4]
    match_index = match_stats_url_suffix.split('/')[5]

    try:
        winner_slug_xpath = "//div[@class='player-left-name']/a/@href"
        winner_slug_parsed = xpath_parse(match_tree, winner_slug_xpath)
        winner_slug = winner_slug_parsed[0].split('/')[4]
    except Exception:
        winner_slug = ''

    try:
        loser_slug_xpath = "//div[@class='player-right-name']/a/@href"
        loser_slug_parsed = xpath_parse(match_tree, loser_slug_xpath)
        loser_slug = loser_slug_parsed[0].split('/')[4]
    except Exception:
        loser_slug = ''

    match_id = tourney_year + "-" + tourney_id + "-" + match_index + "-" + round_match_id + "-" + winner_player_id + "-" + loser_player_id    

    # # # # # # # #
    # Match stats #
    # # # # # # # #
    
    try:                
        # Stats Xpaths
        left_stats_xpath = "//td[@class='match-stats-number-left']/span/text()"
        left_stats_parsed = xpath_parse(match_tree, left_stats_xpath)
        left_stats_cleaned = regex_strip_array(left_stats_parsed)

        right_stats_xpath = "//td[@class='match-stats-number-right']/span/text()"
        right_stats_parsed = xpath_parse(match_tree, right_stats_xpath)
        right_stats_cleaned = regex_strip_array(right_stats_parsed)        

        # Ratings Xpaths
        left_ratings_xpath = "//td[@class='match-stats-number-left']/span/a/text()"
        left_ratings_parsed = xpath_parse(match_tree, left_ratings_xpath)
        right_ratings_xpath = "//td[@class='match-stats-number-right']/span/a/text()"
        right_ratings_parsed = xpath_parse(match_tree, right_ratings_xpath)

        # Left stats
        left_serve_rating = int(left_ratings_parsed[0])
        left_aces = int(left_stats_cleaned[2])
        left_double_faults = int(left_stats_cleaned[3])

        left_first_serves_in = int(fraction_stats(left_stats_cleaned[5])[0])
        left_first_serves_total = int(fraction_stats(left_stats_cleaned[5])[1])

        left_first_serve_points_won = int(fraction_stats(left_stats_cleaned[7])[0])
        left_first_serve_points_total = int(fraction_stats(left_stats_cleaned[7])[1])

        left_second_serve_points_won = int(fraction_stats(left_stats_cleaned[9])[0])
        left_second_serve_points_total = int(fraction_stats(left_stats_cleaned[9])[1])

        left_break_points_saved = int(fraction_stats(left_stats_cleaned[11])[0])
        left_break_points_serve_total = int(fraction_stats(left_stats_cleaned[11])[1])

        left_service_points_won = int(fraction_stats(left_stats_cleaned[23])[0])
        left_service_points_total = int(fraction_stats(left_stats_cleaned[23])[1])

        left_return_rating = int(left_ratings_parsed[1])
        left_first_serve_return_won = int(fraction_stats(left_stats_cleaned[16])[0])
        left_first_serve_return_total = int(fraction_stats(left_stats_cleaned[16])[1])

        left_second_serve_return_won = int(fraction_stats(left_stats_cleaned[18])[0])
        left_second_serve_return_total = int(fraction_stats(left_stats_cleaned[18])[1])

        left_break_points_converted = int(fraction_stats(left_stats_cleaned[20])[0])
        left_break_points_return_total = int(fraction_stats(left_stats_cleaned[20])[1])

        left_service_games_played = int(left_stats_cleaned[12])
        left_return_games_played = int(left_stats_cleaned[21])

        left_return_points_won = int(fraction_stats(left_stats_cleaned[25])[0])
        left_return_points_total = int(fraction_stats(left_stats_cleaned[25])[1])

        left_total_points_won = int(fraction_stats(left_stats_cleaned[27])[0])
        left_total_points_total = int(fraction_stats(left_stats_cleaned[27])[1])
        
        # Loser stats
        right_serve_rating = int(right_ratings_parsed[0])
        right_aces = int(right_stats_cleaned[2])
        right_double_faults = int(right_stats_cleaned[3])

        right_first_serves_in = int(fraction_stats(right_stats_cleaned[5])[0])
        right_first_serves_total = int(fraction_stats(right_stats_cleaned[5])[1])

        right_first_serve_points_won = int(fraction_stats(right_stats_cleaned[7])[0])
        right_first_serve_points_total = int(fraction_stats(right_stats_cleaned[7])[1])

        right_second_serve_points_won = int(fraction_stats(right_stats_cleaned[9])[0])
        right_second_serve_points_total = int(fraction_stats(right_stats_cleaned[9])[1])

        right_break_points_saved = int(fraction_stats(right_stats_cleaned[11])[0])
        right_break_points_serve_total = int(fraction_stats(right_stats_cleaned[11])[1])

        right_service_points_won = int(fraction_stats(right_stats_cleaned[23])[0])
        right_service_points_total = int(fraction_stats(right_stats_cleaned[23])[1])

        right_return_rating = int(right_ratings_parsed[1])
        right_first_serve_return_won = int(fraction_stats(right_stats_cleaned[16])[0])
        right_first_serve_return_total = int(fraction_stats(right_stats_cleaned[16])[1])

        right_second_serve_return_won = int(fraction_stats(right_stats_cleaned[18])[0])
        right_second_serve_return_total = int(fraction_stats(right_stats_cleaned[18])[1])

        right_break_points_converted = int(fraction_stats(right_stats_cleaned[20])[0])
        right_break_points_return_total = int(fraction_stats(right_stats_cleaned[20])[1])

        right_service_games_played = int(right_stats_cleaned[12])
        right_return_games_played = int(right_stats_cleaned[21])

        right_return_points_won = int(fraction_stats(right_stats_cleaned[25])[0])
        right_return_points_total = int(fraction_stats(right_stats_cleaned[25])[1])

        right_total_points_won = int(fraction_stats(right_stats_cleaned[27])[0])
        right_total_points_total = int(fraction_stats(right_stats_cleaned[27])[1])

        # # # # # # # # # # # # # # # # # # #
        # Assign stats to winner and loser  #
        # # # # # # # # # # # # # # # # # # #

        # Left player url
        left_player_url_xpath = "//div[@class='player-left-name']/a/@href"
        left_player_url_xpath_parsed = xpath_parse(match_tree, left_player_url_xpath)
            
        # Right player url
        right_player_url_xpath = "//div[@class='player-right-name']/a/@href"
        right_player_url_xpath_parsed = xpath_parse(match_tree, right_player_url_xpath)                

        if left_player_url_xpath_parsed == winner_slug_parsed:
            winner_serve_rating = left_serve_rating
            winner_aces = left_aces
            winner_double_faults = left_double_faults
            winner_first_serves_in = left_first_serves_in
            winner_first_serves_total = left_first_serves_total
            winner_first_serve_points_won = left_first_serve_points_won
            winner_first_serve_points_total = left_first_serve_points_total
            winner_second_serve_points_won = left_second_serve_points_won
            winner_second_serve_points_total = left_second_serve_points_total
            winner_break_points_saved = left_break_points_saved
            winner_break_points_serve_total = left_break_points_serve_total
            winner_service_points_won = left_service_points_won
            winner_service_points_total = left_service_points_total
            winner_return_rating = left_return_rating
            winner_first_serve_return_won = left_first_serve_return_won
            winner_first_serve_return_total = left_first_serve_return_total
            winner_second_serve_return_won = left_second_serve_return_won
            winner_second_serve_return_total = left_second_serve_return_total
            winner_break_points_converted = left_break_points_converted
            winner_break_points_return_total = left_break_points_return_total
            winner_service_games_played = left_service_games_played
            winner_return_games_played = left_return_games_played
            winner_return_points_won = left_return_points_won
            winner_return_points_total = left_return_points_total
            winner_total_points_won = left_total_points_won
            winner_total_points_total = left_total_points_total

            loser_serve_rating = right_serve_rating
            loser_aces = right_aces
            loser_double_faults = right_double_faults
            loser_first_serves_in = right_first_serves_in
            loser_first_serves_total = right_first_serves_total
            loser_first_serve_points_won = right_first_serve_points_won
            loser_first_serve_points_total = right_first_serve_points_total
            loser_second_serve_points_won = right_second_serve_points_won
            loser_second_serve_points_total = right_second_serve_points_total
            loser_break_points_saved = right_break_points_saved
            loser_break_points_serve_total = right_break_points_serve_total
            loser_service_points_won = right_service_points_won
            loser_service_points_total = right_service_points_total
            loser_return_rating = right_return_rating
            loser_first_serve_return_won = right_first_serve_return_won
            loser_first_serve_return_total = right_first_serve_return_total
            loser_second_serve_return_won = right_second_serve_return_won
            loser_second_serve_return_total = right_second_serve_return_total
            loser_break_points_converted = right_break_points_converted
            loser_break_points_return_total = right_break_points_return_total
            loser_service_games_played = right_service_games_played
            loser_return_games_played = right_return_games_played
            loser_return_points_won = right_return_points_won
            loser_return_points_total = right_return_points_total
            loser_total_points_won = right_total_points_won
            loser_total_points_total = right_total_points_total                    

        elif right_player_url_xpath_parsed == winner_slug_parsed:
            winner_serve_rating = right_serve_rating
            winner_aces = right_aces
            winner_double_faults = right_double_faults
            winner_first_serves_in = right_first_serves_in
            winner_first_serves_total = right_first_serves_total
            winner_first_serve_points_won = right_first_serve_points_won
            winner_first_serve_points_total = right_first_serve_points_total
            winner_second_serve_points_won = right_second_serve_points_won
            winner_second_serve_points_total = right_second_serve_points_total
            winner_break_points_saved = right_break_points_saved
            winner_break_points_serve_total = right_break_points_serve_total
            winner_service_points_won = right_service_points_won
            winner_service_points_total = right_service_points_total
            winner_return_rating = right_return_rating
            winner_first_serve_return_won = right_first_serve_return_won
            winner_first_serve_return_total = right_first_serve_return_total
            winner_second_serve_return_won = right_second_serve_return_won
            winner_second_serve_return_total = right_second_serve_return_total
            winner_break_points_converted = right_break_points_converted
            winner_break_points_return_total = right_break_points_return_total
            winner_service_games_played = right_service_games_played
            winner_return_games_played = right_return_games_played
            winner_return_points_won = right_return_points_won
            winner_return_points_total = right_return_points_total
            winner_total_points_won = right_total_points_won
            winner_total_points_total = right_total_points_total

            loser_serve_rating = left_serve_rating
            loser_aces = left_aces
            loser_double_faults = left_double_faults
            loser_first_serves_in = left_first_serves_in
            loser_first_serves_total = left_first_serves_total
            loser_first_serve_points_won = left_first_serve_points_won
            loser_first_serve_points_total = left_first_serve_points_total
            loser_second_serve_points_won = left_second_serve_points_won
            loser_second_serve_points_total = left_second_serve_points_total
            loser_break_points_saved = left_break_points_saved
            loser_break_points_serve_total = left_break_points_serve_total
            loser_service_points_won = left_service_points_won
            loser_service_points_total = left_service_points_total
            loser_return_rating = left_return_rating
            loser_first_serve_return_won = left_first_serve_return_won
            loser_first_serve_return_total = left_first_serve_return_total
            loser_second_serve_return_won = left_second_serve_return_won
            loser_second_serve_return_total = left_second_serve_return_total
            loser_break_points_converted = left_break_points_converted
            loser_break_points_return_total = left_break_points_return_total
            loser_service_games_played = left_service_games_played
            loser_return_games_played = left_return_games_played
            loser_return_points_won = left_return_points_won
            loser_return_points_total = left_return_points_total
            loser_total_points_won = left_total_points_won
            loser_total_points_total = left_total_points_total                          
    except Exception:
        winner_serve_rating = ''
        winner_aces = ''
        winner_double_faults = ''
        winner_first_serves_in = ''
        winner_first_serves_total = ''
        winner_first_serve_points_won = ''
        winner_first_serve_points_total = ''
        winner_second_serve_points_won = ''
        winner_second_serve_points_total = ''
        winner_break_points_saved = ''
        winner_break_points_serve_total = ''
        winner_service_points_won = ''
        winner_service_points_total = ''
        winner_return_rating = ''
        winner_first_serve_return_won = ''
        winner_first_serve_return_total = ''
        winner_second_serve_return_won = ''
        winner_second_serve_return_total = ''
        winner_break_points_converted = ''
        winner_break_points_return_total = ''
        winner_service_games_played = ''
        winner_return_games_played = ''
        winner_return_points_won = ''
        winner_return_points_total = ''
        winner_total_points_won = ''
        winner_total_points_total = ''

        loser_serve_rating = ''
        loser_aces = ''
        loser_double_faults = ''
        loser_first_serves_in = ''
        loser_first_serves_total = ''
        loser_first_serve_points_won = ''
        loser_first_serve_points_total = ''
        loser_second_serve_points_won = ''
        loser_second_serve_points_total = ''
        loser_break_points_saved = ''
        loser_break_points_serve_total = ''
        loser_service_points_won = ''
        loser_service_points_total = ''
        loser_return_rating = ''
        loser_first_serve_return_won = ''
        loser_first_serve_return_total = ''
        loser_second_serve_return_won = ''
        loser_second_serve_return_total = ''
        loser_break_points_converted = ''
        loser_break_points_return_total = ''
        loser_service_games_played = ''
        loser_return_games_played = ''
        loser_return_points_won = ''
        loser_return_points_total = ''
        loser_total_points_won = ''
        loser_total_points_total = ''                    

    # Store data
    output = [match_id, tourney_slug, match_stats_url_suffix, match_time, match_duration, winner_slug, winner_serve_rating, winner_aces, winner_double_faults, winner_first_serves_in, winner_first_serves_total, winner_first_serve_points_won, winner_first_serve_points_total, winner_second_serve_points_won, winner_second_serve_points_total, winner_break_points_saved, winner_break_points_serve_total, winner_service_games_played, winner_return_rating, winner_first_serve_return_won, winner_first_serve_return_total, winner_second_serve_return_won, winner_second_serve_return_total, winner_break_points_converted, winner_break_points_return_total, winner_return_games_played, winner_service_points_won, winner_service_points_total, winner_return_points_won, winner_return_points_total, winner_total_points_won, winner_total_points_total, loser_slug, loser_serve_rating, loser_aces, loser_double_faults, loser_first_serves_in, loser_first_serves_total, loser_first_serve_points_won, loser_first_serve_points_total, loser_second_serve_points_won, loser_second_serve_points_total, loser_break_points_saved, loser_break_points_serve_total, loser_service_games_played, loser_return_rating, loser_first_serve_return_won, loser_first_serve_return_total, loser_second_serve_return_won, loser_second_serve_return_total, loser_break_points_converted, loser_break_points_return_total, loser_return_games_played, loser_service_points_won, loser_service_points_total, loser_return_points_won, loser_return_points_total, loser_total_points_won, loser_total_points_total]
    return output

# # # # # # # # # # #
#                   #
#   MAIN ROUTINE    #
#                   #
# # # # # # # # # # #

# Command line input
year = str(sys.argv[1])

# Setup
year_url = "https://www.atptour.com/en/scores/results-archive?year=" + year
url_prefix = "https://www.atptour.com"

# Tourney count
year_tree = html_parse_tree(year_url)
tourney_details_url_xpath = "//tr[contains(@class, 'tourney-result')][*]/td[8]/a/@href"
tourney_url_suffixes = xpath_parse(year_tree, tourney_details_url_xpath)
tourney_count = len(tourney_url_suffixes)

try: start_index = str(sys.argv[2])
except Exception: start_index = str(0)

try: end_index = str(int(sys.argv[3]) + 1)
except Exception: end_index = str(tourney_count)

# Command line output
print('')
print('Collecting match stats data for ' + '\x1b[0;32;40m' + str(tourney_count) + '\x1b[0m' + ' tournaments:')
print('')
print('Index    Tourney slug           Matches')
print('-----    ------------           -------')

# Iterate through each tournament
match_stats_data_scrape = []
for i in range(int(start_index), int(end_index)):

    # Parse tourney tree
    tourney_url_suffix = tourney_url_suffixes[i]
    tourney_url = url_prefix + tourney_url_suffix
    tourney_tree = html_parse_tree(tourney_url)

    # Extract tourney details
    url_split = tourney_url.split("/")
    tourney_slug = url_split[6]
    tourney_year = url_split[8]
    tourney_id = url_split[7]
    tourney_index = str(i)

    # Tourney round count
    tourney_round_name_xpath = "//table[contains(@class, 'day-table')]/thead/tr/th/text()"
    tourney_round_name_parsed = xpath_parse(tourney_tree, tourney_round_name_xpath)
    tourney_round_count = len(tourney_round_name_parsed)
    
    # Match stats URL XPath
    match_stats_url_xpath = "//table[contains(@class, 'day-table')]/tbody[*]/tr[*]/td[contains(@class, 'day-table-score')]/a/@href"
    match_stats_url_cleaned = xpath_parse(tourney_tree, match_stats_url_xpath)
    # Filter problematic URL's
    match_stats_url_suffixes = []
    for foo in match_stats_url_cleaned:
        if foo.find('//') == -1:
            match_stats_url_suffixes.append(foo)

    # Total match count
    total_matches = len(match_stats_url_suffixes)

    # Output tournaments with different match structure
    if total_matches == 0:
        spacing1 = format_spacing(5, tourney_index)
        spacing2 = format_spacing(19, tourney_slug)
        sys.stdout.write('\r' + tourney_index + spacing1 + '    ' + tourney_slug + spacing2 + '    ' + '\x1b[1;31m' + 'Match structure/stats URL problem' + '\x1b[0m')        
    else:
        # Iterate through each round
        output = []
        match_counter = 0
        alt_counter = 0
        for j in range(0, tourney_round_count):

            # Round order and match count
            round_order = j + 1
            #tourney_round_name = tourney_round_name_parsed[j]
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
                match_stats_url_cleaned = []
                for element in match_stats_url_parsed:
                    if len(element) > 0:
                        match_stats_url_cleaned.append(regex_strip_string(element))
                    else:
                        match_stats_url_cleaned.append("TIEBREAK")
                
                # Scrape match stats data synchronously
                match_urls = []
                if len(match_stats_url_cleaned) > 0:
                    match_counter += 1
                    alt_counter += 1
                    # Match stats URL
                    match_stats_url_suffix = match_stats_url_cleaned[0]
                    match_stats_url_suffix_split = match_stats_url_suffix.split('/')
                    match_urls.append(match_stats_url_suffix)
                    match_stats_url = url_prefix + match_stats_url_suffix

                    # # # # # # # # # # # # # # # # # # #
                    # Use scrape_match_stats() function #
                    # # # # # # # # # # # # # # # # # # #
                    scraped_stats = scrape_match_stats(match_stats_url)
                    
                    # Check for walkovers because it overcounts matches with match stats
                    if scraped_stats[4] == '': match_counter -= 1
            
                    # Store scraped stats
                    match_stats_data_scrape += [scraped_stats]           

                # Command line output for match details
                current_count = str(match_counter)
                spacing1 = format_spacing(5, tourney_index)
                spacing2 = format_spacing(19, tourney_slug)
                percent_completed = '{:.0%}'.format(match_counter/float(total_matches))
                if total_matches != 0:
                    if alt_counter == total_matches and match_counter < total_matches:
                        sys.stdout.write('\r' + '\x1b[1;31m' + tourney_index + spacing1 + '    ' + tourney_slug + spacing2 + '    ' + current_count + "/" + str(total_matches) + " (" + str(percent_completed) + ")" + '\x1b[0m')
                    else:                    
                        sys.stdout.write('\r' + tourney_index + spacing1 + '    ' + tourney_slug + spacing2 + '    ' + current_count + '/' + str(total_matches) + ' (' + str(percent_completed) + ')')
                sys.stdout.flush()

    # Print new line after each tournament
    sys.stdout.write('\n')

    # Output to CSV
    filename = "match_stats_" + year + "_" + start_index + ".csv"
    array2csv(match_stats_data_scrape, filename)




