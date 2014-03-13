import csv
from geocoder.geocoder import Geocoder, GeocoderErrorNotFound, GeocoderErrorMultipleResultsFound

class Processor(object):
    def __init__(self,input,output):
        self.output = output
        self.input = input
        self.geocoders = []

    def add_geocoder(self,name):
        raise NotImplementedError

    def get_input(self,row):
        raise NotImplementedError

    def process(self):
        f = open(self.output,"wb")
        writer = csv.writer(f)

        i = 0
        counter = 0
        with open(self.input,'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            geocoders_name = []

            for row in reader:
                i += 1
                if i == 1:
                    row += ["latitude","longitude","geocoder"]
                    writer.writerow(row)
                    continue

                d = self.get_input(row)

                for geocoder in self.geocoders:
                    latitude = 0
                    longitude = 0
                    try:
                        (latitude,longitude) = geocoder.geocode(d)
                    except GeocoderErrorNotFound, e:
                        #print "No results found for",e
                        pass
                    except GeocoderErrorMultipleResultsFound, e:
                        #print "Multiple results found for",e
                        pass
                    else:
                        # We store the latitude,longitude and the geocoder used
                        row += [latitude,longitude,geocoder.get_name()]
                        counter += 1
                        break
                writer.writerow(row)
        f.close()
        print counter,"geocoded locations out of",(i-1)
