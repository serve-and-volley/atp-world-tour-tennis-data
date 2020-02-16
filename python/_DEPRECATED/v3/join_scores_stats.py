import csv

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

year = '2013'

scores_csv = 'csv/2_match_scores/match_scores_' + year + '.csv'
scores = []
read_csv(scores, scores_csv)

stats_csv = 'csv/3_match_stats/match_stats_' + year + '.csv'
stats = []
read_csv(stats, stats_csv)

stats_prepare = []
for match in stats:
	key = match[1]
	value = match[2:]
	stats_prepare.append([key, value])
stats_assoc = dict(stats_prepare)


scores_stats = []
for match in scores:
	key = match[23]
	try:
		foo = match + stats_assoc[key]
	except Exception:
		foo = match
	#if key != '': foo = match + stats_assoc[key]
	#else: foo = match
	scores_stats.append(foo)

# Add NULL values when there are no match stats
for match in scores_stats:
    if len(match) == 24:
        empty = [None] * 50
        match += empty

filename = 'match_scores_stats_' + year
array2csv(scores_stats, filename)
