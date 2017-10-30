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

csv_files = ['../csv/4_rankings/_to-do/rankings_0_2017-10-23.csv', '../csv/4_rankings/_to-do/rankings_1_2017-10-16.csv', '../csv/4_rankings/_to-do/rankings_2_2017-10-09.csv', '../csv/4_rankings/_to-do/rankings_3_2017-10-02.csv', '../csv/4_rankings/_to-do/rankings_4_2017-09-25.csv', '../csv/4_rankings/_to-do/rankings_5_2017-09-18.csv', '../csv/4_rankings/_to-do/rankings_6_2017-09-11.csv', '../csv/4_rankings/_to-do/rankings_7_2017-08-28.csv', '../csv/4_rankings/_to-do/rankings_8_2017-08-21.csv', '../csv/4_rankings/_to-do/rankings_9_2017-08-14.csv', '../csv/4_rankings/_to-do/rankings_10_2017-08-07.csv', '../csv/4_rankings/_to-do/rankings_11_2017-07-31.csv', '../csv/4_rankings/_to-do/rankings_12_2017-07-24.csv', '../csv/4_rankings/_to-do/rankings_13_2017-07-17.csv', '../csv/4_rankings/_to-do/rankings_14_2017-07-10.csv', '../csv/4_rankings/_to-do/rankings_15_2017-07-03.csv', '../csv/4_rankings/_to-do/rankings_16_2017-06-26.csv', '../csv/4_rankings/_to-do/rankings_17_2017-06-19.csv', '../csv/4_rankings/_to-do/rankings_18_2017-06-12.csv', '../csv/4_rankings/_to-do/rankings_19_2017-05-29.csv', '../csv/4_rankings/_to-do/rankings_20_2017-05-22.csv', '../csv/4_rankings/_to-do/rankings_21_2017-05-15.csv', '../csv/4_rankings/_to-do/rankings_22_2017-05-08.csv', '../csv/4_rankings/_to-do/rankings_23_2017-05-01.csv', '../csv/4_rankings/_to-do/rankings_24_2017-04-24.csv', '../csv/4_rankings/_to-do/rankings_25_2017-04-17.csv', '../csv/4_rankings/_to-do/rankings_26_2017-04-10.csv', '../csv/4_rankings/_to-do/rankings_27_2017-04-03.csv', '../csv/4_rankings/_to-do/rankings_28_2017-03-20.csv', '../csv/4_rankings/_to-do/rankings_29_2017-03-06.csv', '../csv/4_rankings/_to-do/rankings_30_2017-02-27.csv', '../csv/4_rankings/_to-do/rankings_31_2017-02-20.csv', '../csv/4_rankings/_to-do/rankings_32_2017-02-13.csv', '../csv/4_rankings/_to-do/rankings_33_2017-02-06.csv', '../csv/4_rankings/_to-do/rankings_34_2017-01-30.csv', '../csv/4_rankings/_to-do/rankings_35_2017-01-16.csv', '../csv/4_rankings/_to-do/rankings_36_2017-01-09.csv', '../csv/4_rankings/_to-do/rankings_37_2017-01-02.csv']

csv_output = []

for csv_file in csv_files:
    read_csv(csv_output, csv_file)

filename = 'rankings_2017_0-37'
array2csv(csv_output, filename)
