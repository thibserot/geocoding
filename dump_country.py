#!/usr/bin/env python

import optparse,csv

class CountryDumper(object):
    def __init__(self,input,countries,output,row_country):
        self.countries = countries
        self.output = output
        self.input = input
        self.row_country = row_country

    def process(self):
        f = open(self.output,"wb")
        writer = csv.writer(f)

        with open(self.input,'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            i = 0
            for row in reader:
                i += 1
                if i == 1:
                    # We write the header
                    writer.writerow(row)
                    continue
                country = row[self.row_country]
                if country in self.countries:
                    writer.writerow(row)
        f.close()


def main():
    usage = "usage: %prog [options] csv_dump.csv"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-c","--country",dest='countries',help='Country to keep', action="append")
    parser.add_option("-o","--output",dest='output',help='Output file')
    parser.add_option("-r","--row",dest='row_country',help='0-Index of the row to filter on.',type="int",default=4)

    (options,args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Incorrect number of arguments")
    else:
        input = args[0]

    if not options.output:
        parser.error("No output specified")
    if not options.countries:
        parser.error("No country to keep specified")

    countryDumper = CountryDumper(input,options.countries, options.output,options.row_country)

    countryDumper.process()


if __name__ == "__main__":
    main()
