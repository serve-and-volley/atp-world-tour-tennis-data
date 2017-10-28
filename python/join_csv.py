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

csv_files = ['_output/3_match_stats/match_stats_revised_1991-1999.csv', '_output/3_match_stats/match_stats_revised_2000-2009.csv', '_output/3_match_stats/match_stats_revised_2010-2016.csv']

#csv_files = ['_output/2_match_scores/match_scores_1877-1967.csv', '_output/2_match_scores/match_scores_1968-1990.csv', '_output/2_match_scores/match_scores_1991-2016.csv']

csv_output = []

for csv_file in csv_files:
    read_csv(csv_output, csv_file)

filename = 'match_stats_unindexed_1991-2016'
array2csv(csv_output, filename)
