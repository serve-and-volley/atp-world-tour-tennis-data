from scraping import *

def tourneys(tourney_year):

    # Command line input
    year = tourney_year

    # Setup
    year_url = "https://www.atptour.com/en/scores/results-archive?year=" + year
    url_prefix = "https://www.atptour.com"
    year_tree = html_parse_tree(year_url)

    # Tourney names
    tourney_name_xpath = "//tr[contains(@class, 'tourney-result')]/td[3]/a/text()"
    tourney_name_parsed = xpath_parse(year_tree, tourney_name_xpath)
    tourney_names = regex_strip_array(tourney_name_parsed)
    tourney_count = len(tourney_names)

    # Tourney date
    tourney_date_xpath = "//tr[contains(@class, 'tourney-result')]/td[3]/span[contains(@class, 'tourney-dates')]/text()"
    tourney_date_parsed = xpath_parse(year_tree, tourney_date_xpath)
    tourney_dates = regex_strip_array(tourney_date_parsed)

    # Tourney type
    tourney_type_xpath = "//tr[contains(@class, 'tourney-result')]/td[2]/img/@src"
    tourney_types = xpath_parse(year_tree, tourney_type_xpath)

    # Tourney URL suffixes
    tourney_details_url_xpath = "//tr[contains(@class, 'tourney-result')][*]/td[8]/a/@href"
    tourney_url_suffixes = xpath_parse(year_tree, tourney_details_url_xpath)
    stats_available = len(tourney_url_suffixes)

    print('\n' + str(tourney_count) + '/' + str(stats_available) + ' tournament stats available' + '\n')

    for i in range(0, tourney_count):

        tourney_order = i + 1

        if tourney_order < 10: spacing = ' '
        else: spacing = ''

        if i < stats_available:
            print(spacing + str(tourney_order) + ' - ' + tourney_dates[i] + ' - ' + tourney_names[i])
        else:
            print(spacing + '\x1b[1;31m' + str(tourney_order) + ' - ' + tourney_dates[i] + ' - ' + tourney_names[i] + '\x1b[0m')