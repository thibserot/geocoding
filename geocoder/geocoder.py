#!/usr/bin/env python
import os,requests,json
from simplejson.decoder import JSONDecodeError
from math import sin, cos, sqrt, atan2, radians

class GeocoderError(Exception):
    def __init__(self,value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class GeocoderErrorNotFound(GeocoderError):
    pass

class GeocoderErrorMultipleResultsFound(GeocoderError):
    pass


class Geocoder(object):
    def __init__(self):
        pass

    def geocode(self,address):
        raise NotImplementedError
    
    def get_name(self):
        raise NotImplementedError
    
    def get_url(self):
        raise NotImplementedError

    def get_payload(self,input):
        raise NotImplementedError

    def get_param(self,input):
        raise NotImplementedError
    
    def get_filename(self,param):
        raise NotImplementedError

    def getLatLng(self,output,idx=0):
        raise NotImplementedError

    def createMapMatch(self,param,records):
        raise NotImplementedError

    def get_content(self,payload,filename="",force=False):

        if filename != "":
            path = os.path.join(os.path.expanduser("~"),".geocoding",self.get_name())
            if not os.path.exists(path):
                os.makedirs(path)

            filename = os.path.join(path,filename)

        if filename != "" and not force and os.path.exists(filename):
            f = open(filename,"rb")
            txt = f.read()
            f.close()
            output = json.loads(txt)
        else:
            r = requests.get(self.url, params=payload,headers={'referer': 'car/'})
            #print r.url
            try:
                output = r.json()
            except JSONDecodeError, e:
                raise GeocoderErrorNotFound(e)

            txt = json.dumps(output,indent=4)
            f = open(filename,"wb")
            f.write(txt)
            f.close()
        return output



    def compute_distance(self,lat1,lon1,lat2,lon2):
        # Earth radius
        R = 6371.0

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        return distance

    def get_header(self):
        return [self.get_name() + " lat", self.get_name() + " lng"]

    def clean_filename(self,filename):
        filename = filename.replace("/","_")
        filename = filename.replace("\\","_")
        filename = filename.replace("?","_")
        filename = filename.replace("%","_")
        filename = filename.replace("*","_")
        filename = filename.replace(":","_")
        filename = filename.replace("|","_")
        filename = filename.replace("\"","_")
        filename = filename.replace("<","_")
        filename = filename.replace(">","_")
        filename = filename.replace(" ","_")
        return filename

    def geocode(self,input):
        payload = self.get_payload(input)
        param = self.get_param(input)
        
        filename = self.clean_filename(self.get_filename(param))
        output = self.get_content(payload,filename)

        output = self.createMapMatch(param,output)
        if len(output) == 0:
            raise GeocoderErrorNotFound(input)
        elif len(output) > 1:
            raise GeocoderErrorMultipleResultsFound(input)

        return self.getLatLng(output,0)
