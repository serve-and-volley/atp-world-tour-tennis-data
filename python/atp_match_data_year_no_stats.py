# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                                                               #
#   This script scrapes the ATP tennis match data by year.                                                                      #
#   This version doesn't scrape the individual match stats.                                                                     #
#                                                                                                                               #
#   Example of how to run this script on the command line:                                                                      #
#   $ time python atp_match_data_year_no_stats.py 2016                                                                          #
#                                                                                                                               #
#   Examples of a player activity year URL:                                                                                     #
#   - http://www.atpworldtour.com/en/scores/results-archive?year=2016                                                           #
#   - http://www.atpworldtour.com/en/scores/results-archive?year=1877                                                           #
#                                                                                                                               #
#   Note:   This script can only scrape the verstion of the ATP website as of Dec 23, 2016.                                     #
#           If the site layout is redesigned, then all of the XPaths in this script becomes invalid.                            #
#                                                                                                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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

# Command line input
year = str(sys.argv[1])

# Setup
year_url = "http://www.atpworldtour.com/en/scores/results-archive?year=" + year
url_prefix = "http://www.atpworldtour.com"

csv_array = []
header = [['year', ' tourney_name', ' tourney_slug', ' tourney_id', ' tourney_location', ' tourney_dates', ' tourney_singles_draw', ' tourney_doubles_draw', ' tourney_conditions', ' tourney_surface', ' tourney_singles_winner_name', ' tourney_singles_winner_slug', ' tourney_singles_winner_player_id', ' tourney_doubles_winner1_name', ' tourney_doubles_winner1_slug', ' tourney_doubles_winner1_player_id', ' tourney_doubles_winner2_name', ' tourney_doubles_winner2_slug', ' tourney_doubles_winner2_player_id', ' tourney_round_name', ' winner_name', ' winner_slug', ' winner_player_id', ' loser_name', ' loser_slug', ' loser_player_id', ' match_score', ' games_total', ' sets_total', ' tiebreaks_total', ' winner_games_won', ' winner_games_lost', ' winner_sets_won', ' winner_sets_lost', ' winner_tiebreaks_won', ' winner_tiebreaks_lost', ' loser_games_won', ' loser_games_lost', ' loser_sets_won', ' loser_sets_lost', ' loser_tiebreaks_won', ' loser_tiebreaks_lost']]
csv_array = header + csv_array

# XPaths
tourney_title_xpath = "//span[contains(@class, 'tourney-title')]/text()"
tourney_title_parsed = html_parse(year_url, tourney_title_xpath)
tourney_title_cleaned = regex_strip_array(tourney_title_parsed)

tourney_count = len(tourney_title_cleaned)

tourney_location_xpath = "//span[contains(@class, 'tourney-location')]/text()"
tourney_location_parsed = html_parse(year_url, tourney_location_xpath)
tourney_location_cleaned = regex_strip_array(tourney_location_parsed)

tourney_dates_xpath = "//span[contains(@class, 'tourney-dates')]/text()"
tourney_dates_parsed = html_parse(year_url, tourney_dates_xpath)
tourney_dates_cleaned = regex_strip_array(tourney_dates_parsed)

tourney_singles_draw_xpath = "//div[contains(., 'SGL')]/a[1]/span/text()"
tourney_singles_draw_parsed = html_parse(year_url, tourney_singles_draw_xpath)
tourney_singles_draw_cleaned = regex_strip_array(tourney_singles_draw_parsed)

tourney_doubles_draw_xpath = "//div[contains(., 'DBL')]/a[1]/span/text()"
tourney_doubles_draw_parsed = html_parse(year_url, tourney_doubles_draw_xpath)
tourney_doubles_draw_cleaned = regex_strip_array(tourney_doubles_draw_parsed)

tourney_conditions_xpath = "//div[contains(., 'Outdoor') or contains(., 'Indoor')]/text()[normalize-space()]"
tourney_conditions_parsed = html_parse(year_url, tourney_conditions_xpath)
tourney_conditions_cleaned = regex_strip_array(tourney_conditions_parsed)

tourney_surface_xpath = "//div[contains(., 'Outdoor') or contains(., 'Indoor')]/span/text()[normalize-space()]"
tourney_surface_parsed = html_parse(year_url, tourney_surface_xpath)
tourney_surface_cleaned = regex_strip_array(tourney_surface_parsed)

tourney_singles_winner_name_xpath = "//div[contains(@class, 'tourney-detail-winner') and contains(., 'SGL')]/a/text()"
tourney_singles_winner_name_parsed = html_parse(year_url, tourney_singles_winner_name_xpath)
tourney_singles_winner_name_cleaned = regex_strip_array(tourney_singles_winner_name_parsed)

tourney_singles_winner_url_xpath = "//div[contains(@class, 'tourney-detail-winner') and contains(., 'SGL')]/a/@href"
tourney_singles_winner_url_parsed = html_parse(year_url, tourney_singles_winner_url_xpath)

tourney_doubles_winner1_name_xpath = "//div[contains(@class, 'tourney-detail-winner') and contains(., 'DBL')]/a[1]/text()"
tourney_doubles_winner1_name_parsed = html_parse(year_url, tourney_doubles_winner1_name_xpath)
tourney_doubles_winner1_name_cleaned = regex_strip_array(tourney_doubles_winner1_name_parsed)

tourney_doubles_winner2_name_xpath = "//div[contains(@class, 'tourney-detail-winner') and contains(., 'DBL')]/a[2]/text()"
tourney_doubles_winner2_name_parsed = html_parse(year_url, tourney_doubles_winner2_name_xpath)
tourney_doubles_winner2_name_cleaned = regex_strip_array(tourney_doubles_winner2_name_parsed)

tourney_doubles_winner1_url_xpath = "//div[contains(@class, 'tourney-detail-winner') and contains(., 'DBL')]/a[1]/@href"
tourney_doubles_winner1_url_parsed = html_parse(year_url, tourney_doubles_winner1_url_xpath)

tourney_doubles_winner2_url_xpath = "//div[contains(@class, 'tourney-detail-winner') and contains(., 'DBL')]/a[2]/@href"
tourney_doubles_winner2_url_parsed = html_parse(year_url, tourney_doubles_winner2_url_xpath)

tourney_details_url_xpath = "//td[contains(@class, 'tourney-details')]/a/@href"
tourney_details_url_parsed = html_parse(year_url, tourney_details_url_xpath)

# Iterate over each tournament
for i in xrange(0, tourney_count):

    tourney_name = tourney_title_cleaned[i]
    tourney_location = tourney_location_cleaned[i]
    tourney_dates = tourney_dates_cleaned[i]
    tourney_singles_draw = tourney_singles_draw_cleaned[i]
    tourney_doubles_draw = tourney_doubles_draw_cleaned[i]
    tourney_conditions = tourney_conditions_cleaned[i].strip()
    tourney_surface = tourney_surface_cleaned[i]

    tourney_singles_winner_name = tourney_singles_winner_name_cleaned[i]
    tourney_singles_winner_slug = tourney_singles_winner_url_parsed[i].split("/")[3]
    tourney_singles_winner_player_id = tourney_singles_winner_url_parsed[i].split("/")[4]
    
    tourney_doubles_winner1_name = tourney_doubles_winner1_name_cleaned[i]
    tourney_doubles_winner2_name = tourney_doubles_winner2_name_cleaned[i]
    tourney_doubles_winner1_slug = tourney_doubles_winner1_url_parsed[i].split("/")[3]
    tourney_doubles_winner2_slug = tourney_doubles_winner2_url_parsed[i].split("/")[3]
    tourney_doubles_winner1_player_id = tourney_doubles_winner1_url_parsed[i].split("/")[4]
    tourney_doubles_winner2_player_id = tourney_doubles_winner2_url_parsed[i].split("/")[4]

    tourney_details_url = tourney_details_url_parsed[i]
    tourney_slug = tourney_details_url.split("/")[4]
    tourney_id = tourney_details_url.split("/")[5]
    tourney_url = url_prefix + tourney_details_url

    tourney_round_name_xpath = "//table[contains(@class, 'day-table')]/thead/tr/th/text()"
    tourney_round_name_parsed = html_parse(tourney_url, tourney_round_name_xpath)
    tourney_round_count = len(tourney_round_name_parsed)

    # Iterate over each tournament round
    for j in xrange(0, tourney_round_count):
        tourney_round_name = tourney_round_name_parsed[j]
        
        tourney_match_count_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr/td[contains(@class, 'day-table-score')]/a"
        tourney_match_count_parsed = html_parse(tourney_url, tourney_match_count_xpath)
        
        tourney_match_count = len(tourney_match_count_parsed)

        # Iterate over each match
        for k in xrange(0, tourney_match_count):

            winner_player_url_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-name')][1]/a/@href"
            winner_player_url_parsed = html_parse(tourney_url, winner_player_url_xpath)
            winner_player_url = winner_player_url_parsed[0]

            winner_slug = winner_player_url.split("/")[3]
            winner_player_id = winner_player_url.split("/")[4]

            winner_name_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-name')][1]/a/text()"
            winner_name_parsed = html_parse(tourney_url, winner_name_xpath)
            winner_name = winner_name_parsed[0]

            loser_player_url_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-name')][2]/a/@href"
            loser_player_url_parsed = html_parse(tourney_url, loser_player_url_xpath)
            loser_player_url = loser_player_url_parsed[0]

            loser_slug = loser_player_url.split("/")[3]
            loser_player_id = loser_player_url.split("/")[4]            

            loser_name_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-name')][2]/a/text()"
            loser_name_parsed = html_parse(tourney_url, loser_name_xpath)
            loser_name = loser_name_parsed[0]

            # Scraping the match score
            match_score_node_xpath = tourney_match_count_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-score')]/a/node()"
            match_score_node_parsed = html_parse(tourney_url, match_score_node_xpath)

            match_score_text_xpath = tourney_match_count_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-score')]/a/text()"
            match_score_text_parsed = html_parse(tourney_url, match_score_text_xpath)
            
            match_score_tiebreak_xpath = tourney_match_count_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(j+1) + "]/tr[" + str(k+1) + "]/td[contains(@class, 'day-table-score')]/a/sup/text()"
            match_score_tiebreak_parsed = html_parse(tourney_url, match_score_tiebreak_xpath)

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
                    if len(test.group(0)) > 0:
                        games_won += int(match_score_split[k][0])
                        games_lost += int(match_score_split[k][1])                        
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
                    if len(test.group(0)) > 0:
                        if int(match_score_split[k][0]) > int(match_score_split[k][1]):
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
                    if len(test.group(0)) > 0:
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
                    if len(test.group(0)) > 0:
                        if int(match_score_no_tiebreak_array[k][0]) > int(match_score_no_tiebreak_array[k][1]):
                            sets_won += 1
                        else:
                            sets_lost += 1                              
            
            winner_games_won = games_won
            winner_games_lost = games_lost
            winner_sets_won = sets_won
            winner_sets_lost = sets_lost
            winner_tiebreaks_won = tiebreaks_won
            winner_tiebreaks_lost = tiebreaks_lost

            loser_games_won = games_lost
            loser_games_lost = games_won
            loser_sets_won = sets_lost
            loser_sets_lost = sets_won
            loser_tiebreaks_won = tiebreaks_lost
            loser_tiebreaks_lost = tiebreaks_won       

            # Command line output for debugging
            print tourney_name + " | " + tourney_round_name + " | " + winner_name + " def. " + loser_name + " | " + match_score

            # Store the data
            data = [year, tourney_name, tourney_slug, tourney_id, tourney_location, tourney_dates, tourney_singles_draw, tourney_doubles_draw, tourney_conditions, tourney_surface, tourney_singles_winner_name, tourney_singles_winner_slug, tourney_singles_winner_player_id, tourney_doubles_winner1_name, tourney_doubles_winner1_slug, tourney_doubles_winner1_player_id, tourney_doubles_winner2_name, tourney_doubles_winner2_slug, tourney_doubles_winner2_player_id, tourney_round_name, winner_name, winner_slug, winner_player_id, loser_name, loser_slug, loser_player_id, match_score, games_total, sets_total, tiebreaks_total, winner_games_won, winner_games_lost, winner_sets_won, winner_sets_lost, winner_tiebreaks_won, winner_tiebreaks_lost, loser_games_won, loser_games_lost, loser_sets_won, loser_sets_lost, loser_tiebreaks_won, loser_tiebreaks_lost]
            csv_array.append(data)

            # Output to CSV file
            csv_out = open(year + ".csv", 'wb')
            mywriter = csv.writer(csv_out)
            for row in csv_array:
                mywriter.writerow(row)
            csv_out.close()
