import csv

def array2csv(array, filename):
    with open(filename, "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter = ',')
        csvWriter.writerows(array)

def read_csv(array, filename):
    with open(filename, 'rb') as input_file:
        foo = csv.reader(input_file)
        for row in foo:
            array.append(row)
    return array

csv_files = ['2_match_scores/match_scores_2010-2017.csv', '2_match_scores/match_scores_2018-2018.csv', '2_match_scores/match_scores_2019-2019.csv']

csv_output = []

for csv_file in csv_files:
    read_csv(csv_output, csv_file)

filename = 'match_scores_2010-2019.csv'
array2csv(csv_output, filename)
