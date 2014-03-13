#!/usr/bin/env python

import optparse,csv

from processor.city import CityProcessor
from processor.address import AddressProcessor

def main():
    usage = "usage: %prog [options] csv_dump.csv"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-o","--output",dest='output',help='Output file')
    parser.add_option("-g","--geocoder",dest='geocoders',help='Geocoder to use. Possible values: OSM | Google', action="append", default=[] )
    parser.add_option("-t","--type",dest='geocoding_type',help='Type of geocoding to perform. Possible values: City | Address', action="append", default=[] )

    (options,args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Incorrect number of arguments")
    else:
        input = args[0]

    if not options.output:
        parser.error("No output specified")
    
    for geocoding in options.geocoding_type:
        if geocoding == "City":
            geo = CityProcessor(input, options.output)
        elif geocoding == "Address":
            geo = AddressProcessor(input, options.output)
        else:
            parser.error("Unknown geocoding type")

        for geocoder in options.geocoders:
            try:
                geo.add_geocoder(geocoder)
            except NotImplementedError, e:
                parser.error(e)

        geo.process()


if __name__ == "__main__":
    main()
