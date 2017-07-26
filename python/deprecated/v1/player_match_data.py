# Library for storing command line inputs
# Note: Player name must be separated by dashes
# Example of command line input for:
#   player: Bjorn-Borg
#   first year: 1971
#   last year: 1993
#   status: retired
#   command line: python player_match_data.py Bjorn-Borg 1971 1993 retired
import sys

# Storing the command line inputs
player = sys.argv[1]
first_year = int(sys.argv[2])
last_year = int(sys.argv[3])
status = sys.argv[4]

# Generating the URL prefix
if status == "retired":
    temp = player.split("-")
    # For player names of two words
    if len(temp) == 2:
        # First 2 digits of last name
        last2 = temp[1][:2]
        # First digit of first name
        first1 = temp[0][:1]
    # To handle player names of three words
    elif len(temp) == 3:
        last2 = temp[2][:2]
        first1 = temp[0][:1]
    url_prefix = "http://www.atpworldtour.com/Tennis/Players/" + last2 + "/" + first1 + "/" + player + ".aspx?t=pa&y="
else:
    url_prefix = "http://www.atpworldtour.com/Tennis/Players/Top-Players/" + player + ".aspx?t=pa&y="

"""
# Comment out all of the lines ABOVE for custom player name input
# Enter your custom input below
player = "Richard-Pancho-A-Gonzales"
last2 = "Go"
first1 = "R"
url_prefix = "http://www.atpworldtour.com/Tennis/Players/" + last2 + "/" + first1 + "/" + player + ".aspx?t=pa&y="
first_year = 1968
last_year = 1980
"""

# Libraries for HTML scraping
import urllib
from lxml import etree
import StringIO

# # # # # # # # # # # # # # # # # # # # # # #
#   LOCAL FUNCTIONS                         #
#   1.  ascii_replace(your_input)           #
#   2.  get_matches(index, html, tree)      #
#   3.  get_info1(html, tree)               #
#   4.  get_info2(tree)                     #
#   5.  match_stats(match_url, html)        #
# # # # # # # # # # # # # # # # # # # # # # #

# Unicode cleanup function
def ascii_replace(your_input):
    for x in xrange(0, len(your_input)):
        your_input[x] = your_input[x].encode('ascii', 'replace')
        your_input[x] = your_input[x].replace("?", " ")

# Get match info for each tournament using the XPath div index
# Output array contains: round, opponent, ranking, score, stats link
def get_matches(index, html, tree):
    div_index = index + 2
    div_index_string = str(div_index)
    # Round
    xpath = "//div[" + div_index_string + "]/div/table/tbody/tr/td[1]/text()"
    test = tree.xpath(xpath)
    tournament_round = test
    tournament_round.pop(0)
    # Opponents
    html2 = html
    html2 = html2.replace("</a/>", "")
    html2 = html2.replace("</a>", "")
    html2 = html2.replace("<a href=", "")
    tree2 = etree.parse(StringIO.StringIO(html2), parser)
    xpath = "//div[" + div_index_string + "]/div/table/tbody/tr/td[2]/text()"
    test = tree2.xpath(xpath)
    ascii_replace(test)
    for j in xrange(0, len(test)):
        test[j] = test[j].replace("\r\n", "")
        index1 = test[j].find(">") + 1
        test[j] = test[j][index1:]
        test[j] = test[j].strip(" ")
    opponents = test
    opponents.pop(0)
    # Ranking
    xpath = "//div[" + div_index_string + "]/div/table/tbody/tr/td[3]/text()"
    test = tree.xpath(xpath)
    for x in xrange(0, len(test)):
        test[x] = test[x].replace("\r\n", "")
        test[x] = test[x].strip(" ")
    opponent_ranking = test
    opponent_ranking.pop(0)
    # Score
    xpath = "//div[" + div_index_string + "]/div/table/tbody/tr/td[4]/text()"
    test = tree.xpath(xpath)
    ascii_replace(test)
    score = test
    score.pop(0)
    # Stats link
    xpath = "//div[" + div_index_string + "]/div/table/tbody/tr/td[5]/a/@onclick"
    test = tree.xpath(xpath)
    for x in xrange(0, len(test)):
        test[x] = test[x].replace("openWin('", "")
        index = test[x].find("'")
        test[x] = test[x][0:index]
        test[x] = "http://www.atpworldtour.com" + test[x]
    stats_link = test
    # Putting together the match array
    # "round", "opponent", "ranking", "score", "stats link"
    match_array = []
    for j in xrange(0, len(tournament_round)):
        match_array_row = [tournament_round[j], opponents[j], opponent_ranking[j], score[j], stats_link[j]]
        match_array.append(match_array_row)
    return match_array

# Tourney info array part 1: tournament, date, type, surface, draw
def get_info1(html, tree):
    html2 = html
    html2 = html2.replace("<strong>", "")
    html2 = html2.replace("</strong>", "")
    html2 = html2.replace("</a/>", "")
    html2 = html2.replace("</a>", "")
    html2 = html2.replace("<a href=", "")
    tree = etree.parse(StringIO.StringIO(html2), parser)
    xpath = "//div[2]/div[2]/div/div/p/text()"
    test = tree.xpath(xpath)
    ascii_replace(test)
    for x in xrange(0, len(test)):
        index = test[x].find(">") + 1
        test[x] = test[x][index:]
        test[x] = test[x].replace("\r\n\t", "")
        test[x] = test[x].split("; ")
    info1 = test
    return info1

# Tourney info array part 2: null, points, ranking, prize money
def get_info2(tree):
    xpath = "//div[2]/div/div/p/span/text()"
    test = tree.xpath(xpath)
    ascii_replace(test)
    for x in xrange(0, len(test)):
        test[x] = test[x].split(":")
        test[x][1] = test[x][1].replace(", ATP Ranking", "")
        test[x][1] = test[x][1].strip(" ")
        test[x][2] = test[x][2].replace(", Prize Money", "")
        test[x][2] = test[x][2].strip(" ")
        test[x][3] = test[x][3].strip(" ")
    info2 = test
    return info2

# Returns array of match statistics for each match
# The exceptions below are a complete hack due to the GIGO problems of the ATP World Tour website
def match_stats(match_url):
    result = urllib.urlopen(match_url)
    html = result.read()
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO.StringIO(html), parser)
    # tournament XPath
    xpath1 = "//tr[3]/td/a/text()"
    try:
        tournament = tree.xpath(xpath1)[0]
    except Exception:
        tournament = "" 
    # XPath: tournament_round
    xpath2 = "//tr[5]/td/text()"
    try:
        tournament_round = tree.xpath(xpath2)[0]
    except Exception:
        tournament_round = ""
    # XPath: time
    xpath3 = "//tr[7]/td/text()"
    try:
        time = tree.xpath(xpath3)[0]
        time = time.encode('ascii', 'ignore')
        time = time.replace("minutes", "")
    except Exception:
        time = ""
        time = time.encode('ascii', 'ignore')
        time = time.replace("minutes", "")
    # XPath: winner
    xpath4 = "//tr[9]/td/a/text()"
    try:
        winner = tree.xpath(xpath4)[0]
    except Exception:
        winner = ""
    # XPath: player1_name, player2_name
    xpath5 = "//tr[11]/td/a/text()"
    try:
        player1_name = tree.xpath(xpath5)[0]
    except Exception:
        player1_name = ""
    try:
        player2_name = tree.xpath(xpath5)[1]
    except Exception:
        player2_name = ""
    # XPath: player1_nationality, player2_nationality
    xpath7 = "//p/text()"
    try:
        player1_nationality = tree.xpath(xpath7)[0]
    except Exception:
        player1_nationality = ""
    try:
        player2_nationality = tree.xpath(xpath7)[1]
    except Exception:
        player2_nationality = ""  
    # XPath: match statistics
    xpath8 = "//td/text()"
    match_stats_array = tree.xpath(xpath8)
    player1_aces = match_stats_array[13]
    player2_aces = match_stats_array[14]
    player1_double_faults = match_stats_array[16]
    player2_double_faults = match_stats_array[17]
    def cleanup(your_input):
        temp = your_input
        temp = temp.encode('ascii', 'ignore')
        index1 = temp.find("%") + 1
        temp = temp[index1:]
        temp = temp.replace("(", "")
        temp = temp.replace(")", "")
        temp = temp.split("/")
        return temp
  # 1st serve
    player1_1st_serves = match_stats_array[19]
    player1_1st_serves = cleanup(player1_1st_serves)
    player1_1st_serves_in = player1_1st_serves[0]
    try:
        player1_1st_serves_total = player1_1st_serves[1]
    except Exception:
        player1_1st_serves_total = ""
    player2_1st_serves = match_stats_array[20]
    player2_1st_serves = cleanup(player2_1st_serves)
    player2_1st_serves_in = player2_1st_serves[0]
    player2_1st_serves_total = player2_1st_serves[1]
    # 1st serve points won
    player1_1st_serves_won = match_stats_array[22]
    player1_1st_serves_won = cleanup(player1_1st_serves_won)
    player1_1st_serve_points_won = player1_1st_serves_won[0]
    try:
        player1_1st_serve_points_total = player1_1st_serves_won[1]
    except Exception:
        player1_1st_serve_points_total = ""
    player2_1st_serves_won = match_stats_array[23]
    player2_1st_serves_won = cleanup(player2_1st_serves_won)
    player2_1st_serve_points_won = player2_1st_serves_won[0]
    player2_1st_serve_points_total = player2_1st_serves_won[1]
    # 2nd serve points won
    player1_2nd_serves_won = match_stats_array[25]
    player1_2nd_serves_won = cleanup(player1_2nd_serves_won)
    player1_2nd_serve_points_won = player1_2nd_serves_won[0]
    try:
        player1_2nd_serve_points_total = player1_2nd_serves_won[1]
    except Exception:
        player1_2nd_serve_points_total = ""
    player2_2nd_serves_won = match_stats_array[26]
    player2_2nd_serves_won = cleanup(player2_2nd_serves_won)
    try:
        player2_2nd_serve_points_won = player2_2nd_serves_won[0]
    except Exception:
        player2_2nd_serve_points_won = ""
    try:
        player2_2nd_serve_points_total = player2_2nd_serves_won[1]
    except Exception:
        player2_2nd_serve_points_total = ""
    # Break points saved
    player1_break_points = match_stats_array[28]
    player1_break_points = cleanup(player1_break_points)
    player1_break_points_won = player1_break_points[0]
    player1_break_points_total = player1_break_points[1]
    player2_break_points = match_stats_array[29]
    try:
        player2_break_points = cleanup(player2_break_points)
    except Exception:
        player2_break_points = ""
    player2_break_points_won = player2_break_points[0]
    try:
        player2_break_points_total = player2_break_points[1]
    except Exception:
        player2_break_points_total = ""  
    # Service games played
    player1_service_games_played = match_stats_array[31]
    player2_service_games_played = match_stats_array[32]
    # 1st serve return points won
    player1_1st_serve_return_points = match_stats_array[34]
    player1_1st_serve_return_points = cleanup(player1_1st_serve_return_points)
    player1_1st_serve_return_points_won = player1_1st_serve_return_points[0]
    player1_1st_serve_return_points_total = player1_1st_serve_return_points[1]
    player2_1st_serve_return_points = match_stats_array[35]
    player2_1st_serve_return_points = cleanup(player2_1st_serve_return_points)
    player2_1st_serve_return_points_won = player2_1st_serve_return_points[0]
    try:
        player2_1st_serve_return_points_total = player2_1st_serve_return_points[1]
    except Exception:
        player2_1st_serve_return_points_total = ""
    # 2nd serve return points won
    player1_2nd_serve_return_points = match_stats_array[37]
    player1_2nd_serve_return_points = cleanup(player1_2nd_serve_return_points)
    player1_2nd_serve_return_points_won = player1_2nd_serve_return_points[0]
    player1_2nd_serve_return_points_total = player1_2nd_serve_return_points[1]
    player2_2nd_serve_return_points = match_stats_array[38]
    player2_2nd_serve_return_points = cleanup(player2_2nd_serve_return_points)
    player2_2nd_serve_return_points_won = player2_2nd_serve_return_points[0]
    player2_2nd_serve_return_points_total = player2_2nd_serve_return_points[1]
    # Break points converted
    player1_break_points_converted = match_stats_array[40]
    player1_break_points_converted = cleanup(player1_break_points_converted)
    player1_break_points_converted_won = player1_break_points_converted[0]
    player1_break_points_converted_total = player1_break_points_converted[1]
    player2_break_points_converted = match_stats_array[41]
    player2_break_points_converted = cleanup(player2_break_points_converted)
    player2_break_points_converted_won = player2_break_points_converted[0]
    player2_break_points_converted_total = player2_break_points_converted[1]
    # Return games played
    player1_return_games_played = match_stats_array[43]
    player2_return_games_played = match_stats_array[44]
    # Total service points won
    player1_total_service_points = match_stats_array[46]
    player1_total_service_points = cleanup(player1_total_service_points)
    player1_total_service_points_won = player1_total_service_points[0]
    try:
        player1_total_service_points_total = player1_total_service_points[1]
    except Exception:
        player1_total_service_points_total = ""
    try:
        player2_total_service_points = match_stats_array[47]
    except Exception:
        player2_total_service_points = ""
    player2_total_service_points = cleanup(player2_total_service_points)
    player2_total_service_points_won = player2_total_service_points[0]
    try:
        player2_total_service_points_total = player2_total_service_points[1]
    except Exception:
        player2_total_service_points_total = ""
    # Total return points won
    try:
        player1_total_return_points = match_stats_array[49]
    except Exception:
        player1_total_return_points = ""  
    player1_total_return_points = cleanup(player1_total_return_points)
    player1_total_return_points_won = player1_total_return_points[0]
    try:
        player1_total_return_points_total = player1_total_return_points[1]
    except Exception:
        player1_total_return_points_total = ""
    try:
        player2_total_return_points = match_stats_array[50]
    except Exception:
        player2_total_return_points = ""
    player2_total_return_points = cleanup(player2_total_return_points)
    player2_total_return_points_won = player2_total_return_points[0]
    try:
        player2_total_return_points_total = player2_total_return_points[1]
    except Exception:
        player2_total_return_points_total = ""
    # Total points won
    try:
        player1_total_points = match_stats_array[52]
    except Exception:
        player1_total_points = ""  
    player1_total_points = cleanup(player1_total_points)
    player1_total_points_won = player1_total_points[0]
    try:
        player1_total_points_total = player1_total_points[1]
    except Exception:
        player1_total_points_total = ""
    try:
        player2_total_points = match_stats_array[53]
    except Exception:
        player2_total_points = ""
    player2_total_points = cleanup(player2_total_points)
    player2_total_points_won = player2_total_points[0]
    try:
        player2_total_points_total = player2_total_points[1]
    except Exception:
        player2_total_points_total = ""
    # Player1 array
    player1_array = [tournament, tournament_round, time, winner, player1_name, player1_nationality, player1_aces, player1_double_faults, player1_1st_serves_in, player1_1st_serves_total, player1_1st_serve_points_won, player1_1st_serve_points_total, player1_2nd_serve_points_won, player1_2nd_serve_points_total, player1_break_points_won, player1_break_points_total, player1_service_games_played, player1_1st_serve_return_points_won, player1_1st_serve_return_points_total, player1_2nd_serve_return_points_won, player1_2nd_serve_return_points_total, player1_break_points_converted_won, player1_break_points_converted_total, player1_return_games_played, player1_total_service_points_won, player1_total_service_points_total, player1_total_return_points_won, player1_total_return_points_total, player1_total_points_won, player1_total_points_total, player2_name, player2_nationality, player2_aces, player2_double_faults, player2_1st_serves_in, player2_1st_serves_total, player2_1st_serve_points_won, player2_1st_serve_points_total, player2_2nd_serve_points_won, player2_2nd_serve_points_total, player2_break_points_won, player2_break_points_total, player2_service_games_played, player2_1st_serve_return_points_won, player2_1st_serve_return_points_total, player2_2nd_serve_return_points_won, player2_2nd_serve_return_points_total, player2_break_points_converted_won, player2_break_points_converted_total, player2_return_games_played, player2_total_service_points_won, player2_total_service_points_total, player2_total_return_points_won, player2_total_return_points_total, player2_total_points_won, player2_total_points_total]  
    # Getting rid of the unicode: u'%\xa0(/)'
    # because this screws up the CSV writer
    unicode_presence = "no"
    for row in player1_array:
        if row.find(u'%\xa0(/)') != -1:
            unicode_presence = "yes"
    if unicode_presence == "yes":
        for i in xrange(0, len(player1_array)):
            player1_array[i] = ""
    # Getting rid of redundant zeroes
    if player1_array[2] == "0":
        for i in xrange(6, 30):
            player1_array[i] = ""
    if player1_array[2] == "0":
        for i in xrange(32, 56):
            player1_array[i] = ""            
    # Outputting the Player1 array
    return player1_array

# # # # # # # # # # #
#                   #
#   MAIN ROUTINE    #
#                   #
# # # # # # # # # # #

# Array of all of the years to get the data from
years_list = []
difference = last_year - first_year + 1
for x in xrange(0, difference):
    temp = x + first_year
    years_list.append(temp)
  
# Final array: Getting all the data
final_array = []
for row in years_list:
    year = row  
    # Initial reading in the URL
    year_string = str(year)

    # This is the URL for current players
    url = url_prefix + year_string + "&m=s&e=0#"
    result = urllib.urlopen(url)
    html = result.read()
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO.StringIO(html), parser)
    # Pre-array 1 (using the functions)
    array1 = []
    for i in xrange(0, len(get_info1(html, tree))):
        array1_row = [get_info1(html, tree)[i][0], get_info1(html, tree)[i][1], get_info1(html, tree)[i][2], get_info1(html, tree)[i][3], get_info1(html, tree)[i][4], get_info2(tree)[i][1], get_info2(tree)[i][2], get_info2(tree)[i][3], get_matches(i, html, tree)]
        array1.append(array1_row)
    # Pre-array 2
    array2 = []
    for i in xrange(0, len(array1)):
        for j in xrange(0, len(array1[i][8])):
            array2_row = [year, array1[i][0], array1[i][1], array1[i][2], array1[i][3], array1[i][4], array1[i][5], array1[i][6], array1[i][7], array1[i][8][j][0], array1[i][8][j][1], array1[i][8][j][2], array1[i][8][j][3], array1[i][8][j][4]]
            array2.append(array2_row)
    # Match stats array
    match_stats_array = []
    for i in xrange(0, len(array2)):
        match_url = array2[i][13]
        row_array = match_stats(match_url)
        match_stats_array.append(row_array)
    # Line below is for debugging for console input
    # print row_array
    # Final array
    last_year_array = [array2[ix] + match_stats_array[ix] for ix in range(len(array2))]
    final_array.append(last_year_array)
    # Lines below is for debugging for console output
    # for row in final_array:
    #    print row
  
# Output array
output_array = final_array[0]
for i in xrange(1, len(final_array)):
    output_array = output_array + final_array[i]

# Add the CSV headers
headers = [["year", "tournament", "start date", "type", "surface", "draw", "atp points", "atp ranking", "tournament prize money", "round", "opponent", "ranking", "score", "stats link", "tournament", "tournament round", "time", "winner", "player1 name", "player1 nationality", "player1 aces", "player1 double faults", "player1 1st serves in", "player1 1st serves total", "player1 1st serve points won", "player1 1st serve points total", "player1 2nd serve points won", "player1 2nd serve points total", "player1 break points won", "player1 break points total", "player1 service games played", "player1 1st serve return points won", "player1 1st serve return points total", "player1 2nd serve return points won", "player1 2nd serve return points total", "player1 break points converted won", "player1 break points converted total", "player1 return games played", "player1 total service points won", "player1 total service points total", "player1 total return points won", "player1 total return points total", "player1 total points won", "player1 total points total", "player2 name", "player2 nationality", "player2 aces", "player2 double faults", "player2 1st serves in", "player2 1st serves total", "player2 1st serve points won", "player2 1st serve points total", "player2 2nd serve points won", "player2 2nd serve points total", "player2 break points won", "player2 break points total", "player2 service games played", "player2 1st serve return points won", "player2 1st serve return points total", "player2 2nd serve return points won", "player2 2nd serve return points total", "player2 break points converted won", "player2 break points converted total", "player2 return games played", "player2 total service points won", "player2 total service points total", "player2 total return points won", "player2 total return points total", "player2 total points won", "player2 total points total"]]

output_array = headers + output_array

# CSV output
import csv
csv_out = open(player + ".csv", 'wb')
mywriter = csv.writer(csv_out)
for row in output_array:
    mywriter.writerow(row)
csv_out.close()
