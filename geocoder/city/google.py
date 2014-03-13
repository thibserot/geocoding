import difflib
from os import getenv

from geocoder.geocoder import Geocoder, GeocoderError, GeocoderErrorNotFound, GeocoderErrorMultipleResultsFound

class GeocoderGoogle(Geocoder):
    url = "https://maps.googleapis.com/maps/api/geocode/json" 
    CITY_TAGS = [ u'locality', u'political']
    key = getenv("GOOGLE_KEY","")

    def get_name(self):
        return "Google"
    
    def get_filename(self,param):
        filename = "city_" + param["country"] + "__" + param["city"] + ".json"
        return filename

    def get_payload(self,input):
        payload = { "address" : input["citycode"], "components" : "country:" + input["country"], "sensor" : "false", "key" : self.key }
        return payload

    def get_param(self,input):
        param = { "city" : input["citycode"], "country" : input["country"], "postalcode" : input["zipcode"] }
        return param

    def getLatLng(self,output,idx=0):
        geometry = output[idx]["geometry"]["location"]
        return [float(geometry["lat"]),float(geometry["lng"])]


    def createMapMatch(self,input,records):
        mapMatch = {}
        records = records["results"]
        for record in records:
            if "address_components" not in record:
                continue

            country_found = False
            for components in record["address_components"]:
                if "types" not in components:
                    continue
                if "country" in components["types"]:
                    if components["short_name"].lower() == input["country"].lower():
                        country_found = True
                        break
            if country_found:
                already_added = []
                for components in record["address_components"]:
                    if "types" not in components:
                        continue
                    for types in components["types"]:
                        if types in self.CITY_TAGS:
                            name = ""
                            if "short_name" in components:
                                name = components["short_name"].lower()
                                if name not in already_added:
                                    if name not in mapMatch:
                                        mapMatch[name] = []
                                    mapMatch[name] += [record,]
                                    already_added += [name,]
                            if "long_name" in components and components["long_name"].lower() not in already_added:
                                name = components["long_name"].lower()
                                if name not in mapMatch:
                                    mapMatch[name] = []
                                mapMatch[name] += [record,]
                                already_added += [name,]
                            break

        keys = mapMatch.keys()
        city = input["city"].lower()
        # Return the best match with more than 60% similarity
        res = difflib.get_close_matches(city,keys,1)
        if len(res) == 1:
            records = mapMatch[res[0]]
        else:
            records = []

        if len(records) > 1:
            # We try a filter by distance
            i = 0
            max_distance = 0
            for i in range(len(records)):
                lat1 = float(records[i]["geometry"]["location"]["lat"])
                lon1 = float(records[i]["geometry"]["location"]["lng"])
                for j in range(i+1,len(records)):
                    lat2 = float(records[j]["geometry"]["location"]["lat"])
                    lon2 = float(records[j]["geometry"]["location"]["lng"])
                    distance = self.compute_distance(lat1,lon1,lat2,lon2)
                    #print distance
                    if distance > max_distance:
                        max_distance = distance
            #print max_distance
            if max_distance != 0 and max_distance < 20:
                # All results are within a 20km radius,
                # we take the one which is a GEOMETRIC_CENTER if possible
                # Otherwise we take one randomly (the first one)
                res = []
                for record in records:
                    if record["geometry"]["location_type"] == "GEOMETRIC_CENTER":
                        res = [record,]
                        break
                if len(res) > 0:
                    records = res
                else:
                    records = [records[0],]



        return records

