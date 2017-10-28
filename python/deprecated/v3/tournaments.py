import sys
from functions import tournaments, array2csv

# Command line input
start_year = str(sys.argv[1])
end_year = str(sys.argv[2])

# Iterate through the years and scrape tourney data

print ''
print 'Year    Tournaments'
print '----    -----------'

tourney_data = []
for h in xrange(int(start_year), int(end_year) + 1):
    year = str(h)
    tourney_data += tournaments(year)

# Output to CSV
filename = 'tournaments_' + start_year + '-' + end_year
array2csv(tourney_data, filename)
