#!/usr/bin/python

# pylint: disable-all

import sys
import getopt
import json
import csv


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if len(inputfile) > 0:
        with open(inputfile) as inputdata:
            items = json.load(inputdata)
        if len(outputfile) > 0:
            f = csv.writer(open(outputfile, 'wb+'))
            f.writerow(['No', 'Name', 'Normal Price',
                        'Discounted Price', 'Specifications', 'URL'])
            for idx, item in enumerate(items):
                for key in item:
                    if item[key] != None:
                        item[key] = unicode(item[key]).encode('utf-8').strip()
                f.writerow([idx + 1, item['name'], item['normal_price'],
                            item['discounted_price'], item['specs'].replace('\n\n', '\n-----\n'), item['url']])


if __name__ == "__main__":
    main(sys.argv[1:])
