import sys
from lxml import html
import requests
import re
import csv

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

def tournaments(year):
    # Setup
    year_url = "http://www.atptour.com/en/scores/results-archive?year=" + year
    url_prefix = "http://www.atptour.com"

    # HTML tree
    year_tree = html_parse_tree(year_url)

    # Initial XPath to find number of tournaments in a given year
    tourney_titles_xpath = "//span[contains(@class, 'tourney-title')]/text()"
    tourney_titles_parsed = xpath_parse(year_tree, tourney_titles_xpath)
    tourney_titles_cleaned = regex_strip_array(tourney_titles_parsed)

    tourney_count = len(tourney_titles_cleaned)

    # Iterate through each row in the tournaments table
    output = []
    for i in range(0, tourney_count):
        tourney_order = i + 1
        
        # Tournament type
        tourney_type_xpath = "//tr[contains(@class, 'tourney-result')][" + str(i + 1) + "]/td[2]/img[contains(@alt, 'tournament badge')]/@src"
        tourney_type_parsed = xpath_parse(year_tree, tourney_type_xpath)

        if len(tourney_type_parsed) > 0:
            if tourney_type_parsed[0] == '/assets/atpwt/images/tournament/badges/categorystamps_grandslam.png': tourney_type = 'Grand Slam'
            elif tourney_type_parsed[0] == '/assets/atpwt/images/tournament/badges/categorystamps_finals.svg': tourney_type = "ATP Finals"
            elif tourney_type_parsed[0] == '/assets/atpwt/images/tournament/badges/categorystamps_1000.png': tourney_type = "Masters 1000"
            elif tourney_type_parsed[0] == '/assets/atpwt/images/tournament/badges/categorystamps_500.png': tourney_type = "ATP 500"
            elif tourney_type_parsed[0] == '/assets/atpwt/images/tournament/badges/categorystamps_250.png': tourney_type = "ATP 250"
            elif tourney_type_parsed[0] == '/assets/atpwt/images/tournament/badges/categorystamps_lvr.png': tourney_type = "Laver Cup"
            elif tourney_type_parsed[0] == '/assets/atpwt/images/tournament/badges/categorystamps_nextgen.svg': tourney_type = "Next Gen Finals"
            else:
                tourney_type = 'undefined'
        else:
            tourney_type = ''

        # Tournament name, location, and start date
        tourney_info_xpath = "//tr[contains(@class, 'tourney-result')][" + str(i + 1) + "]/td[3]/span/text()"
        tourney_info_parsed = xpath_parse(year_tree, tourney_info_xpath)
        tourney_info_cleaned = regex_strip_array(tourney_info_parsed)

        #tourney_name = tourney_info_cleaned[0].encode('utf-8')
        tourney_name = tourney_info_cleaned[0]
        #tourney_location = tourney_info_cleaned[1].encode('utf-8')
        tourney_location = tourney_info_cleaned[1]
        tourney_date = tourney_info_cleaned[2]
        tourney_year = int(year)
        try:
            tourney_date_split = tourney_date.split('.')
            tourney_month = int(tourney_date_split[1])
            tourney_day = int(tourney_date_split[2])
        except Exception:
            tourney_month = ''
            tourney_day = ''

        # Tournament singles draw
        tourney_singles_draw_xpath = "//tr[contains(@class, 'tourney-result')][" + str(i + 1) + "]/td[4]/div/div[contains(., 'SGL')]/a[1]/span/text()"
        #tourney_singles_draw_xpath = "//tr[contains(@class, 'tourney-result')][" + str(i + 1) + "]/td[4]/div/div/a[1]/span/text()"
        tourney_singles_draw_parsed = xpath_parse(year_tree, tourney_singles_draw_xpath)
        tourney_singles_draw_cleaned = regex_strip_array(tourney_singles_draw_parsed)
        tourney_singles_draw = int(tourney_singles_draw_cleaned[0])
        
        # Tournament doubles draw
        tourney_doubles_draw_xpath = "//tr[contains(@class, 'tourney-result')][" + str(i + 1) + "]/td[4]/div/div[contains(., 'DBL')]/a[2]/span/text()"
        tourney_doubles_draw_parsed = xpath_parse(year_tree, tourney_doubles_draw_xpath)
        tourney_doubles_draw_cleaned = regex_strip_array(tourney_doubles_draw_parsed)
        tourney_doubles_draw = int(tourney_doubles_draw_cleaned[0])
        
        # Tournament conditions
        tourney_conditions_xpath = "//tr[contains(@class, 'tourney-result')][" + str(i + 1) + "]/td[5]/div/div[contains(., 'Outdoor') or contains(., 'Indoor')]/text()[normalize-space()]"
        tourney_conditions_parsed = xpath_parse(year_tree, tourney_conditions_xpath)
        tourney_conditions_cleaned = regex_strip_array(tourney_conditions_parsed)
        try:
            tourney_conditions = tourney_conditions_cleaned[0].strip()
        except Exception:
            tourney_conditions = ''
        
        # Tourneament surface
        tourney_surface_xpath = "//tr[contains(@class, 'tourney-result')][" + str(i + 1) + "]/td[5]/div/div[contains(., 'Outdoor') or contains(., 'Indoor')]/span/text()[normalize-space()]"
        tourney_surface_parsed = xpath_parse(year_tree, tourney_surface_xpath)
        tourney_surface_cleaned = regex_strip_array(tourney_surface_parsed)
        try:
            tourney_surface = tourney_surface_cleaned[0].strip()
        except Exception:
            tourney_surface = ''                

        # Tournament total financial commitment
        tourney_fin_commit_xpath = "//tr[contains(@class, 'tourney-result')][" + str(i + 1) + "]/td[6]/div/div/span/text()"
        tourney_fin_commit_parsed = xpath_parse(year_tree, tourney_fin_commit_xpath)
        tourney_fin_commit_cleaned = regex_strip_array(tourney_fin_commit_parsed)
        
        if len(tourney_fin_commit_cleaned) == 0: 
            tourney_fin_commit_raw = ''
            tourney_fin_commit = ''
            currency = ''

        elif len(tourney_fin_commit_cleaned) > 0:
            #tourney_fin_commit = tourney_fin_commit = tourney_fin_commit_cleaned[0].encode('utf-8')
            tourney_fin_commit_raw = tourney_fin_commit_cleaned[0]
            if tourney_fin_commit_raw[0] == '$': currency = 'USD'
            elif tourney_fin_commit_raw[0] == '£': currency = 'GBP'
            elif tourney_fin_commit_raw[0] == '€': currency = 'EUR'
            elif tourney_fin_commit_raw[0] == 'A': currency = 'AUD'
            else: currency = 'PROBLEM'

            tourney_fin_commit = tourney_fin_commit_raw.replace(',','')
            tourney_fin_commit = tourney_fin_commit.replace('$','')
            tourney_fin_commit = tourney_fin_commit.replace('£','')
            tourney_fin_commit = tourney_fin_commit.replace('€','')
            tourney_fin_commit = tourney_fin_commit.replace('A','')
            tourney_fin_commit = int(tourney_fin_commit)

        else: 
            tourney_fin_commit_raw = 'PROBLEM'
            tourney_fin_commit = ''
            currency = ''

        # Tournament results
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
        singles_winner_name_xpath = "//tr[contains(@class, 'tourney-result')][" + str(i + 1) + "]/td[7]/div[contains(., 'SGL:')]/a/text()"
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
        doubles_winners_name_xpath = "//tr[contains(@class, 'tourney-result')][" + str(i + 1) + "]/td[7]/div[contains(., 'DBL:')]/a/text()"
        doubles_winners_name_parsed = xpath_parse(year_tree, doubles_winners_name_xpath)
        doubles_winners_name_cleaned = regex_strip_array(doubles_winners_name_parsed)

        
        if len(doubles_winners_name_cleaned) == 2:
            doubles_winner_1_name = doubles_winners_name_cleaned[0]
            doubles_winner_2_name = doubles_winners_name_cleaned[1]
        elif len(doubles_winners_name_cleaned) == 1:
            doubles_winner_1_name = doubles_winners_name_cleaned[0]
            doubles_winner_2_name = ''
        else:
            doubles_winner_1_name = ''
            doubles_winner_2_name = ''

        doubles_winners_url_xpath = "//tr[@class = 'tourney-result'][" + str(i + 1) + "]/td/div[contains(., 'DBL:')]/a/@href"
        doubles_winners_url_parsed = xpath_parse(year_tree, doubles_winners_url_xpath)
        if len(doubles_winners_url_parsed) == 2:
            doubles_winner_1_url = doubles_winners_url_parsed[0]
            doubles_winner_1_url_split = doubles_winner_1_url.split('/')
            doubles_winner_1_player_slug = doubles_winner_1_url_split[3]
            doubles_winner_1_player_id = doubles_winner_1_url_split[4]

            doubles_winner_2_url = doubles_winners_url_parsed[1]
            doubles_winner_2_url_split = doubles_winner_2_url.split('/')
            doubles_winner_2_player_slug = doubles_winner_2_url_split[3]
            doubles_winner_2_player_id = doubles_winner_2_url_split[4]

        elif len(doubles_winners_url_parsed) == 1:
            doubles_winner_1_url = doubles_winners_url_parsed[0]
            doubles_winner_1_url_split = doubles_winner_1_url.split('/')
            doubles_winner_1_player_slug = doubles_winner_1_url_split[3]
            doubles_winner_1_player_id = doubles_winner_1_url_split[4]

            doubles_winner_2_url = ''
            doubles_winner_2_player_slug = ''
            doubles_winner_2_player_id = ''   
                                    
        else:
            doubles_winner_1_url = ''
            doubles_winner_1_player_slug = ''
            doubles_winner_1_player_id = ''

            doubles_winner_2_url = ''
            doubles_winner_2_player_slug = ''
            doubles_winner_2_player_id = ''   
        
        # Store data
        tourney_year_id = str(year) + '-' + tourney_id
        output.append([tourney_year_id, tourney_order, tourney_type, tourney_name, tourney_id, tourney_slug, tourney_location, tourney_date, year, tourney_month, tourney_day, tourney_singles_draw, tourney_doubles_draw, tourney_conditions, tourney_surface, tourney_fin_commit_raw, currency, tourney_fin_commit, tourney_url_suffix, singles_winner_name, singles_winner_url, singles_winner_player_slug, singles_winner_player_id, doubles_winner_1_name, doubles_winner_1_url, doubles_winner_1_player_slug, doubles_winner_1_player_id, doubles_winner_2_name, doubles_winner_2_url, doubles_winner_2_player_slug, doubles_winner_2_player_id])
    
    # Output progress
    print(year + '    ' + str(tourney_count))
    
    # Output data
    return output

# # # # # # # # # # #
#                   #
#   MAIN ROUTINE    #
#                   #
# # # # # # # # # # #

# Command line input
start_year = str(sys.argv[1])
end_year = str(sys.argv[2])

# Iterate through the years and scrape tourney data

print('')
print('Year    Tournaments')
print('----    -----------')

tourney_data = []
for h in range(int(start_year), int(end_year) + 1):
    year = str(h)
    tourney_data += tournaments(year)

# Output to CSV
filename = 'tournaments_' + start_year + '-' + end_year + '.csv'
array2csv(tourney_data, filename)