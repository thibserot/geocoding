from os import getenv
from geocoder.geocoder import Geocoder

class GeocoderGoogle(Geocoder):
    url = "https://maps.googleapis.com/maps/api/geocode/json" 
    key = getenv("GOOGLE_KEY","")

    def get_name(self):
        return "Google"
    
    def get_filename(self,param):
        filename = "address_" + param["country"] + "__" + param["city"] + "__" + param["street"] + ".json"
        return filename

    def get_payload(self,input):
        payload = { 
                "address" :  (input["street_num"] + " " + input["street"] + " " + input["zipcode"] + " " + input["citycode"]).strip(), 
                "components" : "country:" + input["country"], 
                "sensor" : "false", 
                "key" : self.key 
                }
        return payload

    def get_param(self,input):
        param = { 
                "city" : input["citycode"], 
                "country" : input["country"], 
                "postalcode" : input["zipcode"],
                "street" : (input["street_num"] + " " + input["street"]).strip(),
                }
        return param

    def getLatLng(self,output,idx=0):
        geometry = output[idx]["geometry"]["location"]
        return [float(geometry["lat"]),float(geometry["lng"])]


    def createMapMatch(self,input,records):
        return records["results"]
 
