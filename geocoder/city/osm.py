import difflib
from os import getenv
from geocoder.geocoder import Geocoder, GeocoderError, GeocoderErrorNotFound, GeocoderErrorMultipleResultsFound

class GeocoderOSM(Geocoder):
    url = getenv("OSM_URL","http://localhost/nominatim/search.php")

    # Those tags must be sorted by order of importance for the second filter by area size to work
    CITY_TAGS = [ u'city', u'town', u'village', u'hamlet' ]
    
    def get_name(self):
        return "OSM"

    def get_payload(self,input):
        payload = { "city" : input["citycode"], "country" : input["country"], "postalcode" : input["zipcode"], "format" : "json", "addressdetails" : 1 }
        return payload

    def get_param(self,input):
        param = { "city" : input["citycode"], "country" : input["country"], "postalcode" : input["zipcode"] }
        return param

    def get_filename(self,param):
        filename = "city_" + param["country"] + "__" + param["city"] + ".json"
        return filename

    def getLatLng(self,output,idx=0):
        return [float(output[idx]["lat"]),float(output[idx]["lon"])]

    def createMapMatch(self,param,records):
        mapMatch = {}
        for record in records:
            if "address" in record:
                try:
                    country_code = record["address"]["country_code"]
                    if country_code.lower() != param["country"].lower():
                        continue
                except KeyError,e:
                    print "No country found"
                    continue
                for k in record["address"]:
                    if k in self.CITY_TAGS:
                        city = record["address"][k].lower()
                        if city not in mapMatch:
                            mapMatch[city] = []
                            
                        mapMatch[city] += [record,]
        keys = mapMatch.keys()
        city = param["city"].lower()
        # Return the best match with more than 60% similarity
        res = difflib.get_close_matches(city,keys,1)
        if len(res) == 1:
            records = mapMatch[res[0]]
        
        if len(records) > 1:
            # We filter by size:
            sizeMap = {}
            for city in self.CITY_TAGS:
                sizeMap[city] = []

            for record in records:
                for city in self.CITY_TAGS:
                    if "address" in record and city in record["address"]:
                        sizeMap[city] += [record,]
            #print json.dumps(sizeMap,indent=4)
            for city in self.CITY_TAGS:
                if len(sizeMap[city]) > 0:
                    records = sizeMap[city]
                    break

        if len(records) > 1:
            # We try a filter by distance
            i = 0
            max_distance = 0
            for i in range(len(records)):
                lat1 = float(records[i]["lat"])
                lon1 = float(records[i]["lon"])
                for j in range(i+1,len(records)):
                    lat2 = float(records[j]["lat"])
                    lon2 = float(records[j]["lon"])
                    distance = self.compute_distance(lat1,lon1,lat2,lon2)
                    #print distance
                    if distance > max_distance:
                        max_distance = distance
            if max_distance != 0 and max_distance < 20:
                # All results are within a 20km radius, we take the one with the most importance
                res = []
                importance = 0
                for record in records:
                    if record["importance"] > importance:
                        res = [record,]
                        importance = record["importance"]
                if len(res) > 0:
                    records = res
        return records
