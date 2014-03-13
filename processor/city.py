
from geocoder.city.osm import GeocoderOSM
from geocoder.city.google import GeocoderGoogle

from .processor import Processor

class CityProcessor(Processor):
    
    def get_input(self,row):
        citycode = row[3]
        zipcode = row[2]
        country = row[4]

        d = { 
                "citycode" : citycode,
                "zipcode" : zipcode,
                "country" : country,
            }
        return d

    def add_geocoder(self,name):
        if name == "OSM":
            self.geocoders += [GeocoderOSM(),]
        elif name == "Google":
            self.geocoders += [GeocoderGoogle(),]
        else:
            raise NotImplementedError("Unknown geocoder:" + name)
