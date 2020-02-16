from lxml import html
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures
import requests
import re
import json
import csv
import sys
import time

def html_parse_tree(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree

def xpath_parse(tree, xpath):
    result = tree.xpath(xpath)
    return result

def regex_strip_string(string):
    string = re.sub('\n', '', string).strip()
    string = re.sub('\r', '', string).strip()
    string = re.sub('\t', '', string).strip()
    return string

def regex_strip_array(array):
    for i in xrange(0, len(array)):
        array[i] = regex_strip_string(array[i]).strip()
    return array

def array2csv(array, filename):
    csv_array = array
    csv_out = open(filename + ".csv", 'wb')
    mywriter = csv.writer(csv_out)
    for row in csv_array:
        mywriter.writerow(row)
    csv_out.close()

def read_csv(array, filename):
    with open(filename, 'rb') as input_file:
        foo = csv.reader(input_file)
        for row in foo:
            array.append(row)
    return array

def format_spacing(max_spacing, variable):
    spacing_count = max_spacing - len(variable)
    output = ''
    for i in xrange(0, spacing_count):
        output += ' '
    return output

def tournaments(year):
    # Setup
    year_url = "http://www.atpworldtour.com/en/scores/results-archive?year=" + year
    url_prefix = "http://www.atpworldtour.com"

    # HTML tree
    year_tree = html_parse_tree(year_url)

    # XPaths
    tourney_title_xpath = "//span[contains(@class, 'tourney-title')]/text()"
    tourney_title_parsed = xpath_parse(year_tree, tourney_title_xpath)
    tourney_title_cleaned = regex_strip_array(tourney_title_parsed)

    tourney_count = len(tourney_title_cleaned)

    tourney_location_xpath = "//span[contains(@class, 'tourney-location')]/text()"
    tourney_location_parsed = xpath_parse(year_tree, tourney_location_xpath)
    tourney_location_cleaned = regex_strip_array(tourney_location_parsed)

    tourney_dates_xpath = "//span[contains(@class, 'tourney-dates')]/text()"
    tourney_dates_parsed = xpath_parse(year_tree, tourney_dates_xpath)
    tourney_dates_cleaned = regex_strip_array(tourney_dates_parsed)

    tourney_singles_draw_xpath = "//div[contains(., 'SGL')]/a[1]/span/text()"
    tourney_singles_draw_parsed = xpath_parse(year_tree, tourney_singles_draw_xpath)
    tourney_singles_draw_cleaned = regex_strip_array(tourney_singles_draw_parsed)

    tourney_doubles_draw_xpath = "//div[contains(., 'DBL')]/a[1]/span/text()"
    tourney_doubles_draw_parsed = xpath_parse(year_tree, tourney_doubles_draw_xpath)
    tourney_doubles_draw_cleaned = regex_strip_array(tourney_doubles_draw_parsed)

    tourney_conditions_xpath = "//div[contains(., 'Outdoor') or contains(., 'Indoor')]/text()[normalize-space()]"
    tourney_conditions_parsed = xpath_parse(year_tree, tourney_conditions_xpath)
    tourney_conditions_cleaned = regex_strip_array(tourney_conditions_parsed)

    tourney_surface_xpath = "//div[contains(., 'Outdoor') or contains(., 'Indoor')]/span/text()[normalize-space()]"
    tourney_surface_parsed = xpath_parse(year_tree, tourney_surface_xpath)
    tourney_surface_cleaned = regex_strip_array(tourney_surface_parsed)

    tourney_fin_commit_xpath = "//td[contains(@class, 'fin-commit')]/div/div/span/text()"
    tourney_fin_commit_parsed = xpath_parse(year_tree, tourney_fin_commit_xpath)
    tourney_fin_commit_cleaned = regex_strip_array(tourney_fin_commit_parsed)    

    output = []
    for i in xrange(0, tourney_count):
        tourney_order = i + 1

        # Assign variables
        tourney_name = tourney_title_cleaned[i].encode('utf-8')
        tourney_location = tourney_location_cleaned[i].encode('utf-8')
        tourney_dates = tourney_dates_cleaned[i]
        tourney_singles_draw = tourney_singles_draw_cleaned[i]
        tourney_doubles_draw = tourney_doubles_draw_cleaned[i]
        try:
            tourney_conditions = tourney_conditions_cleaned[i].strip()
            tourney_surface = tourney_surface_cleaned[i]
        except Exception:
            tourney_conditions = ''
            tourney_surface = ''

        if len(tourney_fin_commit_cleaned[i]) > 0:
            tourney_fin_commit = tourney_fin_commit_cleaned[i].encode('utf-8')
        else:
            tourney_fin_commit = ''

        # Tourney URL's
        tourney_details_url_xpath = "//tr[contains(@class, 'tourney-result')][" + str(i + 1) + "]/td[8]/a/@href"
        tourney_details_url_parsed = xpath_parse(year_tree, tourney_details_url_xpath)

        if len(tourney_details_url_parsed) > 0:
            tourney_url_suffix = tourney_details_url_parsed[0]
            tourney_url_split = tourney_url_suffix.split('/')
            tourney_slug = tourney_url_split[4]
            tourney_id = tourney_url_split[5]
        else:
            tourney_url_suffix = ''
            tourney_slug = ''
            tourney_id = ''    

        # Singles winner info
        singles_winner_name_xpath = "//tr[@class = 'tourney-result'][" + str(i + 1) + "]/td/div[contains(., 'SGL:')]/a/text()"
        singles_winner_name_parsed = xpath_parse(year_tree, singles_winner_name_xpath)
        singles_winner_name_cleaned = regex_strip_array(singles_winner_name_parsed)
        if len(singles_winner_name_cleaned) > 0: 
            singles_winner_name = singles_winner_name_cleaned[0]
            singles_winner_url_xpath = "//tr[@class = 'tourney-result'][" + str(i + 1) + "]/td/div[contains(., 'SGL:')]/a/@href"
            singles_winner_url_parsed = xpath_parse(year_tree, singles_winner_url_xpath)
            if len(singles_winner_url_parsed) > 0: 
                singles_winner_url = singles_winner_url_parsed[0]
                singles_winner_url_split = singles_winner_url.split('/')
                singles_winner_player_slug = singles_winner_url_split[3]
                singles_winner_player_id = singles_winner_url_split[4]
            else:
                singles_winner_url = ''
                singles_winner_player_slug = ''
                singles_winner_player_id = ''            
        else: # Case where tourney missing winner name but has a tourney URL
            if tourney_url_suffix != '':
                # Check tourney URL for Finals match winner
                tourney_url = url_prefix + tourney_url_suffix
                tourney_tree = html_parse_tree(tourney_url)
                missing_winner_name_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[*]/td[contains(@class, 'day-table-name')][1]/a/text()"
                missing_winner_name_parsed = xpath_parse(tourney_tree, missing_winner_name_xpath)
                if len(missing_winner_name_parsed) > 0: singles_winner_name = missing_winner_name_parsed[0]
                else:  singles_winner_name = ''
                missing_winner_url_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[*]/td[contains(@class, 'day-table-name')][1]/a/@href"
                missing_winner_url_parsed = xpath_parse(tourney_tree, missing_winner_url_xpath)
                if len(missing_winner_url_parsed) > 0:
                    singles_winner_url = missing_winner_url_parsed[0]
                    singles_winner_url_split = singles_winner_url.split('/')
                    singles_winner_player_slug = singles_winner_url_split[3]
                    singles_winner_player_id = singles_winner_url_split[4]                    
                else:
                    singles_winner_url = ''
                    singles_winner_player_slug = ''
                    singles_winner_player_id = ''          
            else: # Case where tourney is missing URL
                singles_winner_name = ''
                singles_winner_url = ''
                singles_winner_player_slug = ''
                singles_winner_player_id = '' 

        # Doubles winners info
        doubles_winners_name_xpath = "//tr[@class = 'tourney-result'][" + str(i + 1) + "]/td/div[contains(., 'DBL:')]/a/text()"
        doubles_winners_name_parsed = xpath_parse(year_tree, doubles_winners_name_xpath)
        doubles_winners_name_cleaned = regex_strip_array(doubles_winners_name_parsed)
        if len(doubles_winners_name_cleaned) > 0:
            doubles_winner_1_name = doubles_winners_name_cleaned[0]
            doubles_winner_2_name = doubles_winners_name_cleaned[1]
        else:
            doubles_winner_1_name = ''
            doubles_winner_2_name = ''

        doubles_winners_url_xpath = "//tr[@class = 'tourney-result'][" + str(i + 1) + "]/td/div[contains(., 'DBL:')]/a/@href"
        doubles_winners_url_parsed = xpath_parse(year_tree, doubles_winners_url_xpath)
        if len(doubles_winners_url_parsed) > 0:
            doubles_winner_1_url = doubles_winners_url_parsed[0]
            doubles_winner_1_url_split = doubles_winner_1_url.split('/')
            doubles_winner_1_player_slug = doubles_winner_1_url_split[3]
            doubles_winner_1_player_id = doubles_winner_1_url_split[4]

            doubles_winner_2_url = doubles_winners_url_parsed[1]
            doubles_winner_2_url_split = doubles_winner_2_url.split('/')
            doubles_winner_2_player_slug = doubles_winner_2_url_split[3]
            doubles_winner_2_player_id = doubles_winner_2_url_split[4]
        else:
            doubles_winner_1_url = ''
            doubles_winner_1_player_slug = ''
            doubles_winner_1_player_id = ''

            doubles_winner_2_url = ''
            doubles_winner_2_player_slug = ''
            doubles_winner_2_player_id = ''
        # Store data
        output.append([year, tourney_order, tourney_name, tourney_id, tourney_slug, tourney_location, tourney_dates, tourney_singles_draw, tourney_doubles_draw, tourney_conditions, tourney_surface, tourney_fin_commit, tourney_url_suffix, singles_winner_name, singles_winner_url, singles_winner_player_slug, singles_winner_player_id, doubles_winner_1_name, doubles_winner_1_url, doubles_winner_1_player_slug, doubles_winner_1_player_id, doubles_winner_2_name, doubles_winner_2_url, doubles_winner_2_player_slug, doubles_winner_2_player_id])
    # Output progress
    print year + '    ' + str(tourney_count)
    # Output data
    return output

def scrape_year(year):
    # Setup
    year_url = "http://www.atpworldtour.com/en/scores/results-archive?year=" + year
    url_prefix = "http://www.atpworldtour.com"

    # HTML tree
    year_tree = html_parse_tree(year_url)

    # XPaths
    tourney_title_xpath = "//span[contains(@class, 'tourney-title')]/text()"
    tourney_title_parsed = xpath_parse(year_tree, tourney_title_xpath)
    tourney_title_cleaned = regex_strip_array(tourney_title_parsed)

    tourney_count = len(tourney_title_cleaned)

    tourney_location_xpath = "//span[contains(@class, 'tourney-location')]/text()"
    tourney_location_parsed = xpath_parse(year_tree, tourney_location_xpath)
    tourney_location_cleaned = regex_strip_array(tourney_location_parsed)

    tourney_dates_xpath = "//span[contains(@class, 'tourney-dates')]/text()"
    tourney_dates_parsed = xpath_parse(year_tree, tourney_dates_xpath)
    tourney_dates_cleaned = regex_strip_array(tourney_dates_parsed)

    tourney_singles_draw_xpath = "//div[contains(., 'SGL')]/a[1]/span/text()"
    tourney_singles_draw_parsed = xpath_parse(year_tree, tourney_singles_draw_xpath)
    tourney_singles_draw_cleaned = regex_strip_array(tourney_singles_draw_parsed)

    tourney_doubles_draw_xpath = "//div[contains(., 'DBL')]/a[1]/span/text()"
    tourney_doubles_draw_parsed = xpath_parse(year_tree, tourney_doubles_draw_xpath)
    tourney_doubles_draw_cleaned = regex_strip_array(tourney_doubles_draw_parsed)

    tourney_conditions_xpath = "//div[contains(., 'Outdoor') or contains(., 'Indoor')]/text()[normalize-space()]"
    tourney_conditions_parsed = xpath_parse(year_tree, tourney_conditions_xpath)
    tourney_conditions_cleaned = regex_strip_array(tourney_conditions_parsed)

    tourney_surface_xpath = "//div[contains(., 'Outdoor') or contains(., 'Indoor')]/span/text()[normalize-space()]"
    tourney_surface_parsed = xpath_parse(year_tree, tourney_surface_xpath)
    tourney_surface_cleaned = regex_strip_array(tourney_surface_parsed)

    tourney_fin_commit_xpath = "//td[contains(@class, 'fin-commit')]/div/div/span/text()"
    tourney_fin_commit_parsed = xpath_parse(year_tree, tourney_fin_commit_xpath)
    tourney_fin_commit_cleaned = regex_strip_array(tourney_fin_commit_parsed)

    # Iterate over each tournament
    output = []
    tourney_data = []
    tourney_urls = []
    for i in xrange(0, tourney_count):
        tourney_order = i + 1

        # Assign variables
        tourney_name = tourney_title_cleaned[i].encode('utf-8')
        tourney_location = tourney_location_cleaned[i].encode('utf-8')
        tourney_dates = tourney_dates_cleaned[i]
        tourney_singles_draw = tourney_singles_draw_cleaned[i]
        tourney_doubles_draw = tourney_doubles_draw_cleaned[i]
        try:
            tourney_conditions = tourney_conditions_cleaned[i].strip()
            tourney_surface = tourney_surface_cleaned[i]
        except Exception:
            tourney_conditions = ''
            tourney_surface = ''

        if len(tourney_fin_commit_cleaned[i]) > 0:
            tourney_fin_commit = tourney_fin_commit_cleaned[i].encode('utf-8')
        else:
            tourney_fin_commit = ''

        tourney_details_url_xpath = "//tr[contains(@class, 'tourney-result')][" + str(i + 1) + "]/td[8]/a/@href"
        tourney_details_url_parsed = xpath_parse(year_tree, tourney_details_url_xpath)

        if len(tourney_details_url_parsed) > 0:
            tourney_url_suffix = tourney_details_url_parsed[0]
            tourney_url_split = tourney_url_suffix.split('/')
            tourney_slug = tourney_url_split[4]
            tourney_id = tourney_url_split[5]
            tourney_urls.append(tourney_url_suffix)
        else:
            tourney_url_suffix = ''
            tourney_slug = ''
            tourney_id = ''
            tourney_urls.append(tourney_url_suffix)

            print ''
            print 'Tournaments with missing match info...'
            print 'Year    Order    Tournament'
            print '----    -----    ----------'

            spacing_count = 5 - len(str(tourney_order))
            spacing = ''
            for j in xrange(0, spacing_count):
                spacing += ' '

            print year + '    ' + str(tourney_order) + spacing +  '    ' + tourney_name     

        # Store data        
        tourney_data.append([year, tourney_order, tourney_name, tourney_id, tourney_slug, tourney_location, tourney_dates, tourney_singles_draw, tourney_doubles_draw, tourney_conditions, tourney_surface, tourney_fin_commit])

    output = [tourney_data, tourney_urls]
    return output
    
def scrape_tourney(tourney_url_suffix):
    url_prefix = "http://www.atpworldtour.com"
    tourney_url = url_prefix + tourney_url_suffix

    url_split = tourney_url.split("/")
    tourney_slug = url_split[6]

    # Tourney tree
    tourney_tree = html_parse_tree(tourney_url)     

    tourney_round_name_xpath = "//table[contains(@class, 'day-table')]/thead/tr/th/text()"
    tourney_round_name_parsed = xpath_parse(tourney_tree, tourney_round_name_xpath)
    tourney_round_count = len(tourney_round_name_parsed)

    match_urls = []
    match_data = []
    # Iterate through each round    
    for i in xrange(0, tourney_round_count):
        round_order = i + 1

        tourney_round_name = tourney_round_name_parsed[i]

        round_match_count_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr/td[contains(@class, 'day-table-score')]/a"
        round_match_count_parsed = xpath_parse(tourney_tree, round_match_count_xpath)
        round_match_count = len(round_match_count_parsed)
        
        winner_name_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[*]/td[contains(@class, 'day-table-name')][1]/a/text()"
        winner_name_parsed = xpath_parse(tourney_tree, winner_name_xpath)
              
        winner_url_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[*]/td[contains(@class, 'day-table-name')][1]/a/@href"
        winner_url_parsed = xpath_parse(tourney_tree, winner_url_xpath)

        loser_name_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[*]/td[contains(@class, 'day-table-name')][2]/a/text()"
        loser_name_parsed = xpath_parse(tourney_tree, loser_name_xpath)

        loser_url_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i +1) + "]/tr[*]/td[contains(@class, 'day-table-name')][2]/a/@href"
        loser_url_parsed = xpath_parse(tourney_tree, loser_url_xpath)

        # Match scores
        match_scores_text_xpath = tourney_match_count_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[*]/td[contains(@class, 'day-table-score')]/a/node()"
        match_scores_text_parsed = xpath_parse(tourney_tree, match_scores_text_xpath)

        # Fixing tiebreak problem
        match_scores_cleaned = []
        for element in match_scores_text_parsed:
            if len(element) > 0:
                match_scores_cleaned.append(regex_strip_string(element))
            else:
                match_scores_cleaned.append("TIEBREAK")
        
        concat_match_scores = ""
        element_count = len(match_scores_cleaned)
        for j in xrange(0,  element_count - 1):
            concat_match_scores += match_scores_cleaned[j] + "::"
        concat_match_scores += match_scores_cleaned[element_count - 1]

        fix_concat_match_scores = concat_match_scores.replace("::TIEBREAK::", " ")
        match_scores = fix_concat_match_scores.split('::')

        # Iterate through each match
        for j in xrange(0, round_match_count):
            match_order = j + 1

            # Winner
            winner_name = winner_name_parsed[j].encode('utf-8')
            winner_url = winner_url_parsed[j]
            winner_url_split = winner_url.split('/')
            winner_slug = winner_url_split[3]
            winner_player_id = winner_url_split[4]            

            # Loser
            loser_name = loser_name_parsed[j].encode('utf-8')
            try:
                loser_url = loser_url_parsed[j]
                loser_url
                loser_url_split = loser_url.split('/')
                loser_slug = loser_url_split[3]
                loser_player_id = loser_url_split[4]
            except Exception:
                loser_url = ''
                loser_slug = ''
                loser_player_id = ''
            
            # Match score
            match_score = match_scores[j].strip()

            # Match stats URL
            match_stats_url_xpath = tourney_match_count_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[" + str(j + 1) + "]/td[contains(@class, 'day-table-score')]/a/@href"
            match_stats_url_parsed = xpath_parse(tourney_tree, match_stats_url_xpath)
            match_stats_url_cleaned = []
            for element in match_stats_url_parsed:
                if len(element) > 0:
                    match_stats_url_cleaned.append(regex_strip_string(element))
                else:
                    match_stats_url_cleaned.append("TIEBREAK")
            
            if len(match_stats_url_cleaned) > 0:
                match_stats_url_suffix = match_stats_url_cleaned[0]
                match_stats_url_suffix_split = match_stats_url_suffix.split('/')
                tourney_long_slug = match_stats_url_suffix_split[3]
                #tourney_match_id = match_stats_url_split[10]
                match_urls.append(match_stats_url_suffix)
            else:
                match_stats_url_suffix = ''
                tourney_long_slug = ''

            # Store data
            match_data.append([tourney_long_slug, tourney_round_name, round_order, match_order, winner_name, winner_player_id, winner_slug, loser_name, loser_player_id, loser_slug, match_score, match_stats_url_suffix])
            #time.sleep(.100)       

    output = [match_data, match_urls]
    return output

def scrape_match_stats(match_url_suffix):
    url_prefix = "http://www.atpworldtour.com"
    match_stats_url = url_prefix + match_url_suffix

    # Match tree
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

    # Match stats
    match_stats_xpath = "//*[@id='matchStatsData']/text()"
    match_stats_parsed = xpath_parse(match_tree, match_stats_xpath)
    match_stats_cleaned = regex_strip_string(match_stats_parsed[0])
    json_string = match_stats_cleaned
    json_data = json.loads(json_string)

    # Winner stats
    winner_aces = json_data[0]["playerStats"]["Aces"]
    winner_double_faults = json_data[0]["playerStats"]["DoubleFaults"]

    winner_first_serves_in = json_data[0]["playerStats"]["FirstServeDividend"]
    winner_first_serves_total = json_data[0]["playerStats"]["FirstServeDivisor"]

    winner_first_serve_points_won = json_data[0]["playerStats"]["FirstServePointsWonDividend"]
    winner_first_serve_points_total = json_data[0]["playerStats"]["FirstServePointsWonDivisor"]

    winner_second_serve_points_won = json_data[0]["playerStats"]["SecondServePointsWonDividend"]
    winner_second_serve_points_total = json_data[0]["playerStats"]["SecondServePointsWonDivisor"]

    winner_break_points_saved = json_data[0]["playerStats"]["BreakPointsSavedDividend"]
    winner_break_points_serve_total = json_data[0]["playerStats"]["BreakPointsSavedDivisor"]

    winner_service_points_won = json_data[0]["playerStats"]["TotalServicePointsWonDividend"]
    winner_service_points_total = json_data[0]["playerStats"]["TotalServicePointsWonDivisor"]

    winner_first_serve_return_won = json_data[0]["playerStats"]["FirstServeReturnPointsDividend"]
    winner_first_serve_return_total = json_data[0]["playerStats"]["FirstServeReturnPointsDivisor"]

    winner_second_serve_return_won = json_data[0]["playerStats"]["SecondServePointsDividend"]
    winner_second_serve_return_total = json_data[0]["playerStats"]["SecondServePointsDivisor"]

    winner_break_points_converted = json_data[0]["playerStats"]["BreakPointsConvertedDividend"]
    winner_break_points_return_total = json_data[0]["playerStats"]["BreakPointsConvertedDivisor"]

    winner_service_games_played = json_data[0]["playerStats"]["ServiceGamesPlayed"]
    winner_return_games_played = json_data[0]["playerStats"]["ReturnGamesPlayed"]

    winner_return_points_won = json_data[0]["playerStats"]["TotalReturnPointsWonDividend"]
    winner_return_points_total = json_data[0]["playerStats"]["TotalReturnPointsWonDivisor"]

    winner_total_points_won = json_data[0]["playerStats"]["TotalPointsWonDividend"]
    winner_total_points_total = json_data[0]["playerStats"]["TotalPointsWonDivisor"]            

    # Loser stats
    loser_aces = json_data[0]["opponentStats"]["Aces"]
    loser_double_faults = json_data[0]["opponentStats"]["DoubleFaults"]

    loser_first_serves_in = json_data[0]["opponentStats"]["FirstServeDividend"]
    loser_first_serves_total = json_data[0]["opponentStats"]["FirstServeDivisor"]

    loser_first_serve_points_won = json_data[0]["opponentStats"]["FirstServePointsWonDividend"]
    loser_first_serve_points_total = json_data[0]["opponentStats"]["FirstServePointsWonDivisor"]

    loser_second_serve_points_won = json_data[0]["opponentStats"]["SecondServePointsWonDividend"]
    loser_second_serve_points_total = json_data[0]["opponentStats"]["SecondServePointsWonDivisor"]

    loser_break_points_saved = json_data[0]["opponentStats"]["BreakPointsSavedDividend"]
    loser_break_points_serve_total = json_data[0]["opponentStats"]["BreakPointsSavedDivisor"]

    loser_service_points_won = json_data[0]["opponentStats"]["TotalServicePointsWonDividend"]
    loser_service_points_total = json_data[0]["opponentStats"]["TotalServicePointsWonDivisor"]

    loser_first_serve_return_won = json_data[0]["opponentStats"]["FirstServeReturnPointsDividend"]
    loser_first_serve_return_total = json_data[0]["opponentStats"]["FirstServeReturnPointsDivisor"]

    loser_second_serve_return_won = json_data[0]["opponentStats"]["SecondServePointsDividend"]
    loser_second_serve_return_total = json_data[0]["opponentStats"]["SecondServePointsDivisor"]

    loser_break_points_converted = json_data[0]["opponentStats"]["BreakPointsConvertedDividend"]
    loser_break_points_return_total = json_data[0]["opponentStats"]["BreakPointsConvertedDivisor"]

    loser_service_games_played = json_data[0]["opponentStats"]["ServiceGamesPlayed"]
    loser_return_games_played = json_data[0]["opponentStats"]["ReturnGamesPlayed"]

    loser_return_points_won = json_data[0]["opponentStats"]["TotalReturnPointsWonDividend"]
    loser_return_points_total = json_data[0]["opponentStats"]["TotalReturnPointsWonDivisor"]

    loser_total_points_won = json_data[0]["opponentStats"]["TotalPointsWonDividend"]
    loser_total_points_total = json_data[0]["opponentStats"]["TotalPointsWonDivisor"]

    # Store data
    output = [match_url_suffix, match_time, match_duration, winner_aces, winner_double_faults, winner_first_serves_in, winner_first_serves_total, winner_first_serve_points_won, winner_first_serve_points_total, winner_second_serve_points_won, winner_second_serve_points_total, winner_break_points_saved, winner_break_points_serve_total, winner_service_points_won, winner_service_points_total, winner_first_serve_return_won, winner_first_serve_return_total, winner_second_serve_return_won, winner_second_serve_return_total, winner_break_points_converted, winner_break_points_return_total, winner_service_games_played, winner_return_games_played, winner_return_points_won, winner_return_points_total, winner_total_points_won, winner_total_points_total, loser_aces, loser_double_faults, loser_first_serves_in, loser_first_serves_total, loser_first_serve_points_won, loser_first_serve_points_total, loser_second_serve_points_won, loser_second_serve_points_total, loser_break_points_saved, loser_break_points_serve_total, loser_service_points_won, loser_service_points_total, loser_first_serve_return_won, loser_first_serve_return_total, loser_second_serve_return_won, loser_second_serve_return_total, loser_break_points_converted, loser_break_points_return_total, loser_service_games_played, loser_return_games_played, loser_return_points_won, loser_return_points_total, loser_total_points_won, loser_total_points_total]

    return output

def synchronous(url_array, parsing_function, tourney_index, tourney_slug):
    results = []
    match_counter = 0
    for match_url in url_array:
        scrape_match_stats_output = [tourney_index]
        scrape_match_stats_output += parsing_function(match_url)
        results.append(scrape_match_stats_output)

        # Output
        match_counter += 1
        current_count = str(match_counter)
        total_matches = len(url_array)
        percent_completed = '{:.0%}'.format(match_counter/float(total_matches))
        spacing1 = format_spacing(5, tourney_index)
        spacing2 = format_spacing(15, tourney_slug)
        sys.stdout.write('\r' + tourney_index + spacing1 + '    ' + tourney_slug + spacing2 + '    ' + current_count + "/" + str(total_matches) + " (" + str(percent_completed) + ")")
        sys.stdout.flush()

        # Pause to prevent timeouts
        #time.sleep(1)         
    print ""
    return results

def asynchronous(url_array, parsing_function, tourney_index, tourney_slug):
    URLS = url_array

    with ProcessPoolExecutor(max_workers = 4) as executor:
        future_results = {executor.submit(parsing_function, url): url for url in URLS}

        results = []
        match_counter = 0
        for future in concurrent.futures.as_completed(future_results):
            scrape_match_stats_output = [tourney_index]
            scrape_match_stats_output += future.result()
            results.append(scrape_match_stats_output)

            # Output
            match_counter += 1
            current_count = str(match_counter)
            total_matches = len(url_array)
            percent_completed = '{:.0%}'.format(match_counter/float(total_matches))
            spacing1 = format_spacing(5, tourney_index)
            spacing2 = format_spacing(15, tourney_slug)
            sys.stdout.write('\r' + tourney_index + spacing1 + '    ' + tourney_slug + spacing2 + '    ' + current_count + "/" + str(total_matches) + " (" + str(percent_completed) + ")")
            sys.stdout.flush()            

            # Pause to prevent timeouts
            #time.sleep(1) 

    print ""
    return results