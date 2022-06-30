from typing_extensions import Self
from django.http import Http404
import requests
import json
from rest_framework.response import Response
from django.core import exceptions

from rest_framework import status
from rest_framework.views import APIView
from inspiraAssignment.settings import MBTA_URL
from collections import defaultdict

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
    
    def get_name(self, object):
        return self.get_attribute(object, 'name')

    def stops_count(self, object):
        data = self.mbtaapi_request_data('/stops?filter[route]={}'.format(self.get_id(object)))
        return data
    
    def stops_data(self, object):
        return {
            "id": self.get_id(object),
            "name": self.get_name(object)
        }
        
    def get_no_of_stop(self, object):
        no_of_st = self.stops_count(object)
        return {
            "id": self.get_id(object),
            "long_name":self.get_longname(object),
            "stops": len(no_of_st),
        }
    
    def get_no_of_stoplist(self, object):
        no_of_st = self.stops_count(object)
        return {
            "id": self.get_id(object),
            "long_name":self.get_longname(object),
            "stops": len(no_of_st),
            "stop_list": no_of_st
        }
    def get_all_stops_routes(self, object):
        return {
            "id": self.get_id(object),
            "long_name":self.get_longname(object),
            "stop_list": self.data_respresent(self.stops_data, self.stops_count(object))
        }

    def data_respresent(self, function, data,):
        return list(map(function, data))
    
    def stop_with_route(self, routes):
        stopsRoute = {}
        for route in routes:
            for stop in route['stop_list']:
                if stop["name"] not in stopsRoute:
                    stopsRoute[stop["name"]] = set()
                stopsRoute[stop["name"]].add(stop["name"])
        return stopsRoute
    
    def func_route_station(self, func, lst1, lst2):
        return [func(a, b) for (a, b) in zip(lst1, lst2)]

    def func_route_stops(self, stoplist):
        return [stop['name'] for stop in stoplist]
    
    def BFS_SP(self, graph, start, goal):
        explored = []
        
        queue = [[start]]
        
        if start == goal:
            return "Same Station"
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if isinstance(node, dict):
                node = node["name"]

            if node not in explored:
                neighbours = graph[node]
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    if neighbour["name"] == goal:
                        # print("Shortest path = ", *new_path)
                        return new_path
                explored.append(node)

        return "path doesn't exists"




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
        # if not "route_stops" in request.query_params :
        #     raise exceptions.ValidationError("route_stops not given please pass in the api most/fewest")

        if "type" in request.query_params :
            if request.query_params.get('type') in ['0', 0]:
                data = self.mbtaapi_request_data('/routes?filter[type]=0')
            elif request.query_params.get('type') in ['1', 1]:
                data = self.mbtaapi_request_data('/routes?filter[type]=1')
            elif request.query_params.get('type') == '0,1':
                data = self.mbtaapi_request_data('/routes?filter[type]=0,1')
        else:
            data = self.mbtaapi_request_data('/routes?filter[type]=0,1')
        if "route_stops" in request.query_params:
            data = self.data_respresent(self.get_no_of_stop, data)
            if request.query_params.get('route_stops') == 'most':
                data = max(data, key=lambda x:x['stops'])
            elif request.query_params.get('route_stops') == 'fewest':
                data = min(data, key=lambda x:x['stops'])
        else:
            # raise exceptions.ValidationError("route_stops not given please pass in the api most/fewest")
            data = self.data_respresent(self.get_no_of_stoplist, data)
            for route in data:
                for stop in route['stop_list']:
                    if stop['id'] not in updatelist:
                        updatelist[stop['id']] = []
                    updatelist[stop['id']].append(route['long_name'])
            data = dict(filter(lambda x: len(x[1]) > 1, updatelist.items()))

        return Response(data, status=status.HTTP_200_OK)


class ToAndFromStops(APIView, ParentFunctions):
    """
        The input will be 2 stops, what is the best way to shortest way to reach the desination
    """

    @ratelimit(key=lambda g, r: r.META.get('HTTP_X_CLUSTER_CLIENT_IP',
                                       rate='10/m'))
    def get(self, request, format=None):
        if not "start" in request.query_params or not "end" in request.query_params :
            return Response({
                "errors":[{
                    "start": "Start parameter is missing",
                    "end": "End parameter is missing"
                }],
                "message": "request parameter are missing start or end"
            }, status=status.Http404)

        data = self.mbtaapi_request_data('/routes?filter[type]=0,1')
        data = self.data_respresent(self.get_all_stops_routes, data)

        graph = defaultdict(list)
        for route in data:
            stoplist = route.pop('stop_list')
            func =  lambda src, dst: (src, dst, {'route': route})
            nodes = self.func_route_station(func, stoplist, stoplist[1:])

            for node in nodes:
                a,b,c = node
                a["route"] = c["route"]["long_name"]
                b["route"] = c["route"]["long_name"]
                graph[a["name"]].append(b) 
                graph[b["name"]].append(a)         

        # direction = self.BFS_SP(graph, 'Ashmont', 'Arlington')
        direction = self.BFS_SP(graph, request.query_params["start"], request.query_params["end"])

        if isinstance(direction, list):
            direction = [i["name"]+ " ( "+i["route"]+ ")" if isinstance(i, dict) else i for i in direction]

        return Response(direction, status=status.HTTP_200_OK)
