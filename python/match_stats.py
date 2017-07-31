import sys
from functions import html_parse_tree, xpath_parse, synchronous, asynchronous, scrape_match_stats, array2csv, format_spacing

# Command line input
year = str(sys.argv[1])
start_index = str(sys.argv[2])

# Setup
year_url = "http://www.atpworldtour.com/en/scores/results-archive?year=" + year
url_prefix = "http://www.atpworldtour.com"

# STEP 1: Parse tourney URLs
year_tree = html_parse_tree(year_url)
tourney_details_url_xpath = "//tr[contains(@class, 'tourney-result')][*]/td[8]/a/@href"
tourney_url_suffixes = xpath_parse(year_tree, tourney_details_url_xpath)
tourney_count = len(tourney_url_suffixes)

print ''
print 'Collecting match stats data for ' + '\x1b[0;32;40m' + str(tourney_count) + '\x1b[0m' + ' tournaments:'
print ''
print 'Index    Tourney slug       Matches'
print '-----    ------------       -------'

# Iterate through each tournament
match_stats_data_scrape = []
for i in xrange(int(start_index), tourney_count):

    # Parse tourney tree
    tourney_url = url_prefix + tourney_url_suffixes[i]
    tourney_tree = html_parse_tree(tourney_url)

    # Extract tourney details
    tourney_index = str(i)
    tourney_url_suffix_split = tourney_url_suffixes[i].split('/')
    tourney_slug = tourney_url_suffix_split[4]

    # Match stats URL XPath
    match_stats_url_xpath = tourney_match_count_xpath = "//table[contains(@class, 'day-table')]/tbody[*]/tr[*]/td[contains(@class, 'day-table-score')]/a/@href"
    match_stats_url_cleaned = xpath_parse(tourney_tree, match_stats_url_xpath)

    # Filter problematic URL's
    match_stats_url_suffixes = []
    for foo in match_stats_url_cleaned:
        if foo.find('//') == -1:
            match_stats_url_suffixes.append(foo)

    # STEP 2: Parse match stats
    if len(match_stats_url_suffixes) > 0:

        # Parse match stats asynchronously
        match_stats_data_scrape += asynchronous(match_stats_url_suffixes, scrape_match_stats, tourney_index, tourney_slug)

        # Parse match stats synchronously
        #match_stats_data_scrape += synchronous(match_stats_url_suffixes, scrape_match_stats, tourney_index, tourney_slug)

    else:
        spacing1 = format_spacing(5, tourney_index)
        spacing2 = format_spacing(15, tourney_slug)
        print tourney_index + spacing1 + '    ' + tourney_slug + spacing2 + '    Match stats URL problems'

    # STEP 3: Output to CSV
    filename = "match_stats_" + year + "_" + start_index
    array2csv(match_stats_data_scrape, filename)
