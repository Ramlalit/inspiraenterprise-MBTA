import requests
import json
from rest_framework.response import Response
from django.core import exceptions

from rest_framework import status
from rest_framework.views import APIView
from inspiraAssignment.settings import MBTA_URL

from ratelimit.decorators import ratelimit


"""
    class will return list of long name from the mbta api

    it also contain the filter with type
    if ?type=0
        it will return list of Light rail (type = 0)
    elif ?type=1
        it will return list of Heavy rail (type = 1)
    elif ?type=0,1
        it will return list of Light rail and heavy rail (type = 0,1)
"""

class ParentFunctions():
    
    def mbtaapi_request_data(self, query=None):
        """
            Request the data from the MBTA Api
        """
        if query:
            url = MBTA_URL + query
        else:
            url = MBTA_URL
        response = requests.get(url)
        if response.status_code == 200:
            payload = json.loads(response.text)
        else:
            payload = {
                "data":[]
            }
        return payload["data"]

    def get_attribute(self, object, attr):
        """
            attar: will be dynamic name to get any data from the object
        """
        return object['attributes'][attr]

    def get_id(self, object):
        return object['id']

    def get_longname(self, object):
        return self.get_attribute(object, 'long_name')

    def stops_count(self, object):
        data = self.mbtaapi_request_data('/stops?filter[route]={}'.format(self.get_id(object)))
        return data
        
    def get_no_of_stop(self, object):
        no_of_st = self.stops_count(object)
        return {
            "id": self.get_id(object),
            "long_name":self.get_longname(object),
            "stops": len(no_of_st),
            "stop_list": no_of_st
        }

    def data_respresent(self, function, data,):
        return list(map(function, data))



class LightAndHeavyRailList(APIView, ParentFunctions):
    """
        List of light and heavy rail

        The ratelimit will added, the user can request the api not more then 10 in per minute

    """

    @ratelimit(key=lambda g, r: r.META.get('HTTP_X_CLUSTER_CLIENT_IP',
                                       rate='10/m'))
    def get(self, request, format=None):

        if "type" in request.query_params :
            if request.query_params.get('type') in ['0', 0]:
                data = self.mbtaapi_request_data('/routes?filter[type]=0')
            elif request.query_params.get('type') in ['1', 1]:
                data = self.mbtaapi_request_data('/routes?filter[type]=1')
            elif request.query_params.get('type') == '0,1':
                data = self.mbtaapi_request_data('/routes?filter[type]=0,1')
        else:
            data = self.mbtaapi_request_data('/routes')
        
        data = self.data_respresent(self.get_longname, data)
        return Response(data, status=status.HTTP_200_OK)




class MostAndFewest(APIView, ParentFunctions):
    """
        List of light and heavy rail

        The ratelimit will added, the user can request the api not more then 10 in per minute
    """

    @ratelimit(key=lambda g, r: r.META.get('HTTP_X_CLUSTER_CLIENT_IP',
                                       rate='10/m'))
    def get(self, request, format=None):
        updatelist = {}
        if not "route_stops" in request.query_params :
            raise exceptions.ValidationError("route_stops not given please pass in the api most/fewest")

        if "type" in request.query_params :
            if request.query_params.get('type') in ['0', 0]:
                data = self.mbtaapi_request_data('/routes?filter[type]=0')
            elif request.query_params.get('type') in ['1', 1]:
                data = self.mbtaapi_request_data('/routes?filter[type]=1')
            elif request.query_params.get('type') == '0,1':
                data = self.mbtaapi_request_data('/routes?filter[type]=0,1')
        else:
            data = self.mbtaapi_request_data('/routes?filter[type]=0,1')
        
        data = self.data_respresent(self.get_no_of_stop, data)


        if request.query_params.get('route_stops') == 'most':
            data = max(data, key=lambda x:x['stops'])
        elif request.query_params.get('route_stops') == 'fewest':
            data = max(data, key=lambda x:x['stops'])
        else:
            # raise exceptions.ValidationError("route_stops not given please pass in the api most/fewest")
            for route in data:
                for stop in route['stop_list']:
                    if stop['id'] not in updatelist:
                        updatelist[stop['id']] = []
                    updatelist[stop['id']].append(route['long_name'])

            data = list(filter(lambda x: len(x) > 1, updatelist.values()))

        return Response(data, status=status.HTTP_200_OK)
