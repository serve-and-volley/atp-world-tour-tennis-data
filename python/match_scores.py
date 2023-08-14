
# # # # # # # # #
#               #
#   FUNCTIONS   #
#               #
# # # # # # # # #

from scraping import *

def scrape_year(year):
    # Setup
    year_url = "http://www.atptour.com/en/scores/results-archive?year=" + year
    url_prefix = "http://www.atptour.com"

    # HTML tree
    year_tree = html_parse_tree(year_url)

    # XPaths
    tourney_title_xpath = "//span[contains(@class, 'tourney-title')]/text()"
    tourney_title_parsed = xpath_parse(year_tree, tourney_title_xpath)
    tourney_title_cleaned = regex_strip_array(tourney_title_parsed)

    # If tournament not found in <span> tags try find in <a> tags
    if len(tourney_title_cleaned) == 0:
        tourney_titles_xpath = "//a[contains(@class, 'tourney-title')]/text()"
        tourney_titles_parsed = xpath_parse(year_tree, tourney_titles_xpath)
        tourney_title_cleaned = regex_strip_array(tourney_titles_parsed)

    tourney_count = len(tourney_title_cleaned)

    # Iterate over each tournament
    output = []
    tourney_data = []
    tourney_urls = []
    problem_tourneys = []
    for i in range(0, tourney_count):
        tourney_order = i + 1
        tourney_name = tourney_title_cleaned[i]

        # Assign variables
        tourney_details_url_xpath = "//tr[contains(@class, 'tourney-result')][" + str(i + 1) + "]/td[8]/a/@href"
        tourney_details_url_parsed = xpath_parse(year_tree, tourney_details_url_xpath)

        if len(tourney_details_url_parsed) > 0:
            tourney_url_suffix = tourney_details_url_parsed[0]
            tourney_url_split = tourney_url_suffix.split('/')
            tourney_slug = tourney_url_split[4]
            tourney_id = tourney_url_split[5]
            tourney_year_id = str(year) + '-' + tourney_id
            tourney_urls.append(tourney_url_suffix)
        else:
            tourney_url_suffix = ''
            tourney_slug = ''
            tourney_id = ''
            tourney_year_id = ''
            tourney_urls.append(tourney_url_suffix)
            problem_tourneys.append([year, tourney_order, tourney_name])

        # Store data
        tourney_data.append([tourney_year_id, tourney_order, tourney_name, tourney_slug, tourney_url_suffix])

    # Print missing info
    if len(problem_tourneys) > 0:
        print('')
        print('Tournaments with missing match info...')
        print('Year    Order    Tournament')
        print('----    -----    ----------')

        for tourney in problem_tourneys:
            year = tourney[0]
            tourney_order = tourney[1]
            tourney_name = tourney[2]

            spacing_count = 5 - len(str(tourney_order))
            spacing = ''
            for j in range(0, spacing_count):
                spacing += ' '
            print(tourney_name)
            print(year + '    ' + str(tourney_order) + spacing +  '    ' + tourney_name)

    # Output data
    output = [tourney_data, tourney_urls]
    return output

def scrape_tourney(tourney_url_suffix):
    url_prefix = "http://www.atptour.com"
    tourney_url = url_prefix + tourney_url_suffix

    url_split = tourney_url.split("/")
    tourney_slug = url_split[6]
    tourney_year = url_split[8]
    tourney_id = url_split[7]

    # Tourney tree
    tourney_tree = html_parse_tree(tourney_url)

    tourney_round_name_xpath = "//table[contains(@class, 'day-table')]/thead/tr/th/text()"
    tourney_round_name_parsed = xpath_parse(tourney_tree, tourney_round_name_xpath)
    tourney_round_count = len(tourney_round_name_parsed)

    # Tourney dates
    try:
        tourney_dates_xpath = "//span[contains(@class, 'tourney-dates')]/text()"
        tourney_dates_parsed = xpath_parse(tourney_tree, tourney_dates_xpath)
        tourney_dates_cleaned = regex_strip_string(tourney_dates_parsed[0])
        tourney_dates_split = tourney_dates_cleaned.split(' - ')
        start_date = tourney_dates_split[0]
        end_date = tourney_dates_split[1]
        start_date_split = tourney_dates_split[0].split('.')
        end_date_split = tourney_dates_split[1].split('.')
        start_year = int(start_date_split[0])
        start_month = int(start_date_split[1])
        start_day = int(start_date_split[2])
        end_year = int(end_date_split[0])
        end_month =  int(end_date_split[1])
        end_day =  int(end_date_split[2])
    except Exception:
        start_date = ''
        start_year = ''
        start_month = ''
        start_day = ''
        end_date = ''
        end_year = ''
        end_month = ''
        end_day = ''

    # Prize money
    prize_money_xpath = "//td[contains(@class, 'prize-money')]/div[2]/div/span/text()"
    prize_money_parsed = xpath_parse(tourney_tree, prize_money_xpath)
    prize_money_cleaned = regex_strip_array(prize_money_parsed)

    if len(prize_money_cleaned) == 0 or prize_money_cleaned[0] == '':
        prize_money_raw = ''
        prize_money = ''
        currency = ''

    elif len(prize_money_cleaned) > 0:
        prize_money_raw = prize_money_cleaned[0]

        if tourney_id == '319' or tourney_id == '306':
            prize_money = prize_money_raw.replace(',', '')
            prize_money = int(re.findall('\d+', prize_money)[0])
            currency = 'EUR'
        else:
            if prize_money_raw[0] == '$': currency = 'USD'
            elif prize_money_raw[0] == '£': currency = 'GBP'
            elif prize_money_raw[0] == '€': currency = 'EUR'
            elif prize_money_raw[0] == 'A': currency = 'AUD'
            else: currency = 'PROBLEM'

            prize_money = prize_money_raw.replace(',', '')
            prize_money = prize_money.replace('$', '')
            prize_money = prize_money.replace('£', '')
            prize_money = prize_money.replace('€', '')
            prize_money = prize_money.replace('A', '')
            prize_money = int(prize_money)

    else:
        prize_money_raw = 'PROBLEM'
        prize_money = ''
        currency = ''

    # Iterate through each round
    match_urls = []
    match_data = []
    for i in range(0, tourney_round_count):
        round_order = i + 1

        tourney_round_name = tourney_round_name_parsed[i]

        #round_match_count_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr/td[contains(@class, 'day-table-score')]/a/@href"
        round_match_count_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr/td[contains(@class, 'day-table-name')][1]/a/text()"
        round_match_count_parsed = xpath_parse(tourney_tree, round_match_count_xpath)
        round_match_count = len(round_match_count_parsed)

        # Iterate through each match
        for j in range(0, round_match_count):
            match_order = j + 1
            round_match_id = str(tourney_round_count - i) + '-' + str(round_match_count - j)

            # Winner
            winner_name_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[" + str(j + 1) + "]/td[contains(@class, 'day-table-name')][1]/a/text()"
            winner_name_parsed = xpath_parse(tourney_tree, winner_name_xpath)

            winner_url_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[" + str(j + 1) + "]/td[contains(@class, 'day-table-name')][1]/a/@href"
            winner_url_parsed = xpath_parse(tourney_tree, winner_url_xpath)

            #winner_name = winner_name_parsed[0].encode('utf-8')
            winner_name = winner_name_parsed[0]
            winner_url = winner_url_parsed[0]
            winner_url_split = winner_url.split('/')
            winner_slug = winner_url_split[3]
            winner_player_id = winner_url_split[4]

            # Loser
            loser_name_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[" + str(j + 1) + "]/td[contains(@class, 'day-table-name')][2]/a/text()"
            loser_name_parsed = xpath_parse(tourney_tree, loser_name_xpath)

            loser_url_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i +1) + "]/tr[" + str(j + 1) + "]/td[contains(@class, 'day-table-name')][2]/a/@href"
            loser_url_parsed = xpath_parse(tourney_tree, loser_url_xpath)

            try:
                #loser_name = loser_name_parsed[0].encode('utf-8')
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

            # Seeds
            winner_seed_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[" + str(j + 1) + "]/td[contains(@class, 'day-table-seed')][1]/span/text()"
            winner_seed_parsed = xpath_parse(tourney_tree, winner_seed_xpath)
            winner_seed_cleaned = regex_strip_array(winner_seed_parsed)
            if len(winner_seed_cleaned) > 0:
                winner_seed = winner_seed_cleaned[0]
            else:
                winner_seed = ''
            winner_seed = winner_seed.replace('(', '')
            winner_seed = winner_seed.replace(')', '')

            loser_seed_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[" + str(j + 1) + "]/td[contains(@class, 'day-table-seed')][2]/span/text()"
            loser_seed_parsed = xpath_parse(tourney_tree, loser_seed_xpath)
            loser_seed_cleaned = regex_strip_array(loser_seed_parsed)
            if len(loser_seed_cleaned) > 0:
                loser_seed = loser_seed_cleaned[0]
            else:
                loser_seed = ''
            loser_seed = loser_seed.replace('(', '')
            loser_seed = loser_seed.replace(')', '')

            # Match score
            match_score_text_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[" + str(j + 1) + "]/td[contains(@class, 'day-table-score')]/a/text()"
            match_score_text_parsed = xpath_parse(tourney_tree, match_score_text_xpath)
            if len(match_score_text_parsed) > 0:
                if len(match_score_text_parsed) == 1:
                    match_score_tiebreaks = '(W/O)'
                    winner_sets_won = ''
                    loser_sets_won = ''
                    winner_games_won = ''
                    loser_games_won = ''
                    winner_tiebreaks_won = ''
                    loser_tiebreaks_won = ''

                else:
                    # Tiebreaks
                    tiebreaks_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[" + str(j + 1) + "]/td[contains(@class, 'day-table-score')]/a/sup/text()"
                    tiebreaks_parsed = xpath_parse(tourney_tree, tiebreaks_xpath)

                    # Fixing tiebreak problem
                    tiebreak_counter = 0
                    match_score_cleaned = []
                    tiebreak_score_cleaned = []

                    for q in range(1, len(match_score_text_parsed)):
                        foo = regex_strip_string(match_score_text_parsed[q])
                        if len(foo) > 0:
                            match_score_cleaned.append(foo)
                            tiebreak_score_cleaned.append(foo)
                        else:
                            match_score_cleaned.append("TIEBREAK")
                            tiebreak_score_cleaned.append("[" + tiebreaks_parsed[tiebreak_counter] + "]")
                            tiebreak_counter += 1

                    # Finalize match scores
                    concat_match_score = ""
                    element_count = len(match_score_cleaned)
                    for k in range(0,  element_count - 1):
                        concat_match_score += match_score_cleaned[k] + "::"
                    concat_match_score += match_score_cleaned[element_count - 1]

                    #fix_concat_match_score = concat_match_score.replace("::TIEBREAK::", " ")
                    fix_concat_match_score = concat_match_score.replace("::TIEBREAK::", "::")
                    fix_concat_match_score = fix_concat_match_score.replace("::TIEBREAK", "")
                    match_score = fix_concat_match_score.split('::')
                    # Finalize tiebreak scores
                    concat_tiebreak_score = ""
                    tiebreak_element_count = len(tiebreak_score_cleaned)
                    for k in range(0, tiebreak_element_count - 1):
                        concat_tiebreak_score += tiebreak_score_cleaned[k] + "::"
                    concat_tiebreak_score += tiebreak_score_cleaned[element_count -1]

                    fix_concat_tiebreak_score = concat_tiebreak_score.replace("::[", "(")
                    fix_concat_tiebreak_score = fix_concat_tiebreak_score.replace("]::", ") ")
                    fix_concat_tiebreak_score = fix_concat_tiebreak_score.replace("]", ")")
                    tiebreak_score = fix_concat_tiebreak_score.split('::')

                    #match_score = match_score[0].strip()
                    match_score = ' '.join(match_score)
                    #match_score_tiebreaks = tiebreak_score[0].strip()
                    match_score_tiebreaks = ' '.join(tiebreak_score)
                    if match_score_tiebreaks.find('(RET)') > 0:
                        match_score_tiebreaks = match_score_tiebreaks.replace('(RET)','').strip()
                        match_score_tiebreaks = match_score_tiebreaks + ' (RET)'

                    winner_sets_won = 0
                    loser_sets_won = 0
                    winner_games_won = 0
                    loser_games_won = 0
                    winner_tiebreaks_won = 0
                    loser_tiebreaks_won = 0
                    match_score_split = match_score.split(' ')

                    for sets in match_score_split:
                        if len(sets) == 2:
                            if sets[0] > sets[1]:
                                winner_sets_won += 1
                                winner_games_won += int(sets[0])
                                loser_games_won += int(sets[1])
                                if sets == '76': winner_tiebreaks_won += 1

                            elif sets[0] < sets[1]:
                                loser_sets_won += 1
                                winner_games_won += int(sets[0])
                                loser_games_won += int(sets[1])
                                if sets == '67': loser_tiebreaks_won += 1

                        elif len(sets) == 3:
                            if sets == '810':
                                loser_sets_won += 1
                                loser_games_won += 10
                                winner_games_won += 8
                            elif sets == '108':
                                winner_sets_won += 1
                                winner_games_won += 10
                                loser_games_won += 8
                            elif sets == '911':
                                loser_sets_won += 1
                                loser_games_won += 11
                                winner_games_won += 9
                            elif sets == '119':
                                winner_sets_won += 1
                                winner_games_won += 11
                                loser_games_won += 9

                        elif len(sets) == 4 and sets.isdigit() == True:
                            if int(sets[0:2]) > int(sets[2:4]):
                                winner_sets_won += 1
                                winner_games_won += int(sets[0:2])
                                loser_games_won += int(sets[2:4])
                            elif int(sets[2:4]) > int(sets[0:2]):
                                loser_sets_won += 1
                                winner_games_won += int(sets[0:2])
                                loser_games_won += int(sets[2:4])

                # Match stats URL
                match_stats_url_xpath = tourney_match_count_xpath = "//table[contains(@class, 'day-table')]/tbody[" + str(i + 1) + "]/tr[" + str(j + 1) + "]/td[contains(@class, 'day-table-score')]/a/@href"
                match_stats_url_parsed = xpath_parse(tourney_tree, match_stats_url_xpath)
                match_stats_url_cleaned = []
                for element in match_stats_url_parsed:
                    if len(element) > 0: match_stats_url_cleaned.append(regex_strip_string(element))
                    #else: match_stats_url_cleaned.append("TIEBREAK")

                # Match id
                if len(match_stats_url_cleaned) > 0:
                    match_stats_url_suffix = match_stats_url_cleaned[0]
                    match_stats_url_suffix_split = match_stats_url_suffix.split('/')
                    match_index = match_stats_url_suffix_split[5]
                    match_urls.append(match_stats_url_suffix)
                else:
                    match_stats_url_suffix = ''
                    match_index = 'NULL'
                match_id = tourney_year + "-" + tourney_id + "-" + match_index + "-" + round_match_id + "-" + winner_player_id + "-" + loser_player_id

                # Store data
                match_data.append([start_date, start_year, start_month, start_day, end_date, end_year, end_month, end_day, currency, prize_money, match_index, tourney_round_name, round_order, match_order, winner_name, winner_player_id, winner_slug, loser_name, loser_player_id, loser_slug, winner_seed, loser_seed, match_score_tiebreaks, winner_sets_won, loser_sets_won, winner_games_won, loser_games_won, winner_tiebreaks_won, loser_tiebreaks_won, match_id, match_stats_url_suffix])
                #time.sleep(.100)

    output = [match_data, match_urls]
    return output

# # # # # # # # # # #
#                   #
#   MAIN ROUTINE    #
#                   #
# # # # # # # # # # #

# Command line input
start_year = input('Enter start year: ')
end_year = input('Enter end year: ')

# STEP 1: Scrape year page
tourney_match = []
for h in range(int(start_year), int(end_year) + 1):

    year = str(h)
    scrape_year_output = scrape_year(year)
    tourney_data_scrape = scrape_year_output[0]
    tourney_urls_scrape = scrape_year_output[1]

    print('')
    print('Scraping match info for ' + str(len(tourney_urls_scrape)) + ' tournaments...')
    print('Year    Order    Tournament                                Matches')
    print('----    -----    ----------                                -------')

    #for i in range(0 , len(tourney_urls_scrape)):
    for i in range(0 , 2):
        if len(tourney_urls_scrape[i]) > 0:
            # STEP 2: Scrape tournament page
            match_data_scrape = []
            match_urls_scrape = []

            scrape_tourney_output = scrape_tourney(tourney_urls_scrape[i])
            match_data_scrape = scrape_tourney_output[0]
            match_urls_scrape = scrape_tourney_output[1]
            #match_counter += len(match_data_scrape)

            # STEP 3: tourney_data + match_data
            for match in match_data_scrape:
                foo = tourney_data_scrape[i] + match
                tourney_match.append(foo)

            spacing_count1 = len('Order') - len(str(tourney_data_scrape[i][1]))
            spacing1 = ''
            for j in range(0, spacing_count1): spacing1 += ' '

            spacing_count2 = 41 - len(tourney_data_scrape[i][2])
            spacing2 = ''
            for j in range(0, spacing_count2): spacing2 += ' '

            if len(match_data_scrape) == 0: print(year + '    ' + '\x1b[1;31m' + str(tourney_data_scrape[i][1]) + spacing1 + '    ' + tourney_data_scrape[i][2] + spacing2 + ' ' + str(len(match_data_scrape)) + '\x1b[0m')
            else: print(year + '    ' + str(tourney_data_scrape[i][1]) + spacing1 + '    ' + tourney_data_scrape[i][2] + spacing2 + ' ' + str(len(match_data_scrape)))

        filename = "match_scores_" + start_year + "-" + end_year + '.csv'
        array2csv(tourney_match, filename)
