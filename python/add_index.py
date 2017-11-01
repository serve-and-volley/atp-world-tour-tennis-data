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

start_index = 91957
input_csv_filename = 'match_stats_2017_0-64.csv'
output_csv_filename = 'match_stats_2017_0-64_INDEXED'

unindexed = []
read_csv(unindexed, input_csv_filename)

indexed = []
for i in xrange(0, len(unindexed)):
    row = [i + start_index] + unindexed[i]
    indexed.append(row)

array2csv(indexed, output_csv_filename)