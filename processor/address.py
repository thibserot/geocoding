import json

from geocoder.address.osm import GeocoderOSM
from geocoder.address.google import GeocoderGoogle

from .processor import Processor


class AddressProcessor(Processor):

    def get_input(self,row):

        street_num = row[0]
        street     = row[1]
        zipcode    = row[2]
        citycode   = row[3]
        country    = row[4]

        d = { 
                "citycode" : citycode,
                "zipcode" : zipcode,
                "country" : country,
                "street_num" : street_num,
                "street" : street
            }

        return d

    def add_geocoder(self,name):
        if name == "OSM":
            self.geocoders += [GeocoderOSM(),]
        elif name == "Google":
            self.geocoders += [GeocoderGoogle(),]
        else:
            raise NotImplementedError("Unknown geocoder:" + name)
