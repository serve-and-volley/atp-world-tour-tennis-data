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

csv_files = ['_incomplete/2013/match_stats_2013_0-15.csv', '_incomplete/2013/match_stats_2013_16-23.csv', '_incomplete/2013/match_stats_2013_24-31.csv', '_incomplete/2013/match_stats_2013_32-34.csv', '_incomplete/2013/match_stats_2013_35-52.csv', '_incomplete/2013/match_stats_2013_53-61.csv', '_incomplete/2013/match_stats_2013_62-63.csv']

csv_output = []

for csv_file in csv_files:
	read_csv(csv_output, csv_file)

filename = 'match_stats_2013'
array2csv(csv_output, filename)
