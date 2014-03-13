from os import getenv
from geocoder.geocoder import Geocoder

class GeocoderOSM(Geocoder):
    url = getenv("OSM_URL","http://localhost/nominatim/search.php")
 
    def get_name(self):
        return "OSM"

    def get_payload(self,input):
        payload = { 
                "city" : input["citycode"], 
                "country" : input["country"], 
                "postalcode" : input["zipcode"], 
                "street" : (input["street_num"] + " " + input["street"]).strip(),
                "format" : "json", 
                "addressdetails" : 1 
                }
        return payload

    def get_param(self,input):
        param = { 
                "city" : input["citycode"], 
                "country" : input["country"], 
                "postalcode" : input["zipcode"], 
                "street" : (input["street_num"] + " " + input["street"]).strip()
                }
        return param

    def get_filename(self,param):
        filename = "address_" + param["country"] + "__" + param["city"] + "__" + param["street"] + ".json"
        return filename

    def getLatLng(self,output,idx=0):
        return [float(output[idx]["lat"]),float(output[idx]["lon"])]


    def createMapMatch(self,param,records):
        return records
