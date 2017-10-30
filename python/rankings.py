import sys
from functions import html_parse_tree, xpath_parse, regex_strip_array, read_csv, array2csv

start_index = int(sys.argv[1])
end_index = int(sys.argv[2])

csv_file = 'weeks.csv'

weeks_list = []
read_csv(weeks_list, csv_file)

print ""
print "Collecting weekly rankings data from " + str(len(weeks_list)) + " weeks..."

print ""
print "Index    Week"
print "-----    ----"

#for h in xrange(index, 1):
#for h in xrange(index, len(weeks_list)):
for h in xrange(start_index, end_index + 1):
    week = weeks_list[h][0]
    week_url = "http://www.atpworldtour.com/en/rankings/singles?rankDate=" + week + "&rankRange=1-3000"

    week_tree = html_parse_tree(week_url)

    player_count_xpath = "//table[@class='mega-table']/tbody/tr/td[@class='rank-cell']/text()"
    player_count_parsed = xpath_parse(week_tree, player_count_xpath)
    player_count_cleaned = regex_strip_array(player_count_parsed)
    player_count = len(player_count_cleaned)

    rank_xpath = "//table[@class='mega-table']/tbody/tr/td[@class='rank-cell']/text()"
    rank_parsed = xpath_parse(week_tree, rank_xpath)
    rank_cleaned = regex_strip_array(rank_parsed)   

    player_url_xpath = "//table[@class='mega-table']/tbody/tr/td[@class='player-cell']/a/@href"
    player_url_parsed = xpath_parse(week_tree, player_url_xpath)
    player_url_cleaned = regex_strip_array(player_url_parsed)

    move_xpath = "//table[@class='mega-table']/tbody/tr/td[@class='move-cell']/div[@class='move-text']/text()"
    move_parsed = xpath_parse(week_tree, move_xpath)
    move_cleaned = regex_strip_array(move_parsed)

    age_xpath = "//table[@class='mega-table']/tbody/tr/td[@class='age-cell']/text()"
    age_parsed = xpath_parse(week_tree, age_xpath)
    age_cleaned = regex_strip_array(age_parsed)

    points_xpath = "//table[@class='mega-table']/tbody/tr/td[@class='points-cell']/a/text()"
    points_parsed = xpath_parse(week_tree, points_xpath)

    tourneys_xpath = "//table[@class='mega-table']/tbody/tr/td[@class='tourn-cell']/a/text()"
    tourneys_parsed = xpath_parse(week_tree, tourneys_xpath)

    rankings = []
    #for i in xrange(1160, 1170):
    for i in xrange(0, player_count):
        rank_text = rank_cleaned[i]
        rank_number = rank_text.replace('T', '')

        player_url = player_url_cleaned[i]
        player_url_split = player_url.split('/')
        player_slug = player_url_split[3]
        player_id = player_url_split[4]

        week_split = week.split('-')
        week_year = int(week_split[0])
        week_month = int(week_split[1])
        week_day = int(week_split[2])

        week_title = week.replace('-','.')

        move = move_cleaned[i]        
        move_up_xpath = "//table[@class='mega-table']/tbody/tr[" + str(i + 1) + "]/td[@class='move-cell']/div[@class='move-up']"
        move_up_parsed = xpath_parse(week_tree, move_up_xpath)
        move_down_xpath = "//table[@class='mega-table']/tbody/tr[" + str(i + 1) + "]/td[@class='move-cell']/div[@class='move-down']"
        move_down_parsed = xpath_parse(week_tree, move_down_xpath)
        if len(move_up_parsed) > 0:
            move_direction = 'up'
        elif len(move_down_parsed) > 0:
            move_direction = 'down'
        else:
            move_direction = ''

        age = age_cleaned[i]
        points = int(points_parsed[i].replace(',', ''))
        tourneys = tourneys_parsed[i]

        data = [week_title, week_year, week_month, week_day, rank_text, rank_number, move, move_direction, age, points, tourneys, player_url, player_slug, player_id]
        rankings.append(data)
        
        filename = 'rankings_' + str(h) + '_' + week
        array2csv(rankings, filename)

    print str(h) + "        " + week