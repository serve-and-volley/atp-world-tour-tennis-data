from lxml import html
import requests
import re
import csv

def html_parse_tree(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree

def xpath_parse(tree, xpath):
    result = tree.xpath(xpath)
    return result

def regex_strip_array(array):
    for i in range(0, len(array)):
        array[i] = regex_strip_string(array[i]).strip()
    return array

def regex_strip_string(string):
    string = re.sub('\n', '', string).strip()
    string = re.sub('\r', '', string).strip()
    string = re.sub('\t', '', string).strip()
    return string

def format_spacing(max_spacing, variable):
    spacing_count = max_spacing - len(variable)
    output = ''
    for i in range(0, spacing_count):
        output += ' '
    return output

def fraction_stats(string):
    string = string.replace('(', '')
    string = string.replace(')', '')
    return string.split('/')

def add2csv(array, filename):
    with open(filename, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(array)

def array2csv(array, filename):
    with open(filename, "w+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter = ',')
        csvWriter.writerows(array)