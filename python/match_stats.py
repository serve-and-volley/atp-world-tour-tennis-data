from match_stats_match_info import tourney_matches
from match_stats_tourney_list import tourneys
from match_stats_players_data_extended import match_data_extended
from match_stats_players_data import match_data
from scraping import add2csv

import chromedriver_autoinstaller
from selenium import webdriver

# User selects year
tourney_year = input('\nEnter year: ')
tourneys(tourney_year)

# User selects tournament
tourney_selected = input('\nEnter tourney number: ')
print('')
tourney_index = int(tourney_selected) - 1
tourney_matches_array = tourney_matches(tourney_year, tourney_index)
match_count = len(tourney_matches_array)
for match_info in tourney_matches_array:
    print(str(match_info[0]) + ' - ' + match_info[1] + ' - ' + match_info[2] + ' - ' + match_info[4])

# User selects match to start scraping
match_selected = input('\nEnter match to start scraping: ')
print('')
match_index = int(match_selected) - 1

url_prefix = 'https://www.atptour.com'
chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

for i in range (match_index, match_count):
    tourney_slug = tourney_matches_array[i][1]
    match_id = tourney_matches_array[i][2]
    match_stats_url_suffix = tourney_matches_array[i][7]
    match_stats_url = url_prefix + match_stats_url_suffix
    
    winner_player_id = tourney_matches_array[i][5]
    loser_player_id = tourney_matches_array[i][6]

    csv_filename = str(tourney_year) + '-' + str(tourney_selected) + '-' + tourney_slug + '-' + str(match_selected) + '.csv'
    extended_csv_filename = str(tourney_year) + '-' + str(tourney_selected) + '-' + tourney_slug + '-' + str(match_selected) + '-extended.csv'

    driver.get(match_stats_url)
    html = driver.page_source
    if html.find('Net points won') > 0:
        if match_data_extended(html, winner_player_id, loser_player_id) == 'MISSING DATA':
            print('\x1b[1;31m' + 'MISSING DATA: ' + str(tourney_matches_array[i][0]) + ' - ' + tourney_matches_array[i][1] + ' - ' + tourney_matches_array[i][2] + ' - ' + tourney_matches_array[i][4] + '\x1b[0m')
        else:
            scraped_data = match_data_extended(html, winner_player_id, loser_player_id)
            csv_row_data = [match_id, tourney_slug, match_stats_url_suffix] + scraped_data[0:56]
            csv_row_data_extended = [match_id, tourney_slug, match_stats_url_suffix] + [scraped_data[2]] + scraped_data[56:66] + [scraped_data[29]] + scraped_data[66:76]
            add2csv(csv_row_data, csv_filename)
            add2csv(csv_row_data_extended, extended_csv_filename)
            print('\x1b[0;36;40m' + str(tourney_matches_array[i][0]) + ' - ' + tourney_matches_array[i][1] + ' - ' + tourney_matches_array[i][2] + ' - ' + tourney_matches_array[i][4] + '\x1b[0m' + ' (plus extended data)')   
    else:
        if match_data(html, winner_player_id, loser_player_id) == 'MISSING DATA':
            print('\x1b[1;31m' + 'MISSING DATA: ' + str(tourney_matches_array[i][0]) + ' - ' + tourney_matches_array[i][1] + ' - ' + tourney_matches_array[i][2] + ' - ' + tourney_matches_array[i][4] + '\x1b[0m')
        else:
            scraped_data = match_data(html, winner_player_id, loser_player_id)
            csv_row_data = [match_id, tourney_slug, match_stats_url_suffix] + scraped_data[0:56]
            add2csv(csv_row_data, csv_filename)
            print('\x1b[0;32;40m' + str(tourney_matches_array[i][0]) + ' - ' + tourney_matches_array[i][1] + ' - ' + tourney_matches_array[i][2] + ' - ' + tourney_matches_array[i][4] + '\x1b[0m')

    
