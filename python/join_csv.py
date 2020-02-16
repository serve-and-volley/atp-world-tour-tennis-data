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

csv_files = ['rankings_2017_0109-1120.csv', 'rankings_0_2017-01-02.csv']

#csv_files = ['rankings_0_2017-11-20.csv', 'rankings_1_2017-11-13.csv', 'rankings_2_2017-11-06.csv', 'rankings_3_2017-10-30.csv', 'rankings_4_2017-10-23.csv', 'rankings_5_2017-10-16.csv', 'rankings_6_2017-10-09.csv', 'rankings_7_2017-10-02.csv', 'rankings_8_2017-09-25.csv', 'rankings_9_2017-09-18.csv', 'rankings_10_2017-09-11.csv', 'rankings_11_2017-08-28.csv', 'rankings_12_2017-08-21.csv', 'rankings_13_2017-08-14.csv', 'rankings_14_2017-08-07.csv', 'rankings_15_2017-07-31.csv', 'rankings_16_2017-07-24.csv', 'rankings_17_2017-07-17.csv', 'rankings_18_2017-07-10.csv', 'rankings_19_2017-07-03.csv', 'rankings_20_2017-06-26.csv', 'rankings_21_2017-06-19.csv', 'rankings_22_2017-06-12.csv', 'rankings_23_2017-05-29.csv', 'rankings_24_2017-05-22.csv', 'rankings_25_2017-05-15.csv', 'rankings_26_2017-05-08.csv', 'rankings_27_2017-05-01.csv', 'rankings_28_2017-04-24.csv', 'rankings_29_2017-04-17.csv', 'rankings_30_2017-04-10.csv', 'rankings_31_2017-04-03.csv', 'rankings_32_2017-03-20.csv', 'rankings_33_2017-03-06.csv', 'rankings_34_2017-02-27.csv', 'rankings_35_2017-02-20.csv', 'rankings_36_2017-02-13.csv', 'rankings_37_2017-02-06.csv', 'rankings_38_2017-01-30.csv', 'rankings_39_2017-01-16.csv', 'rankings_40_2017-01-09.csv']

csv_output = []

for csv_file in csv_files:
    read_csv(csv_output, csv_file)

filename = 'rankings_2017_0102-1120'
array2csv(csv_output, filename)
