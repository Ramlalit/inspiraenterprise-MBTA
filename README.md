# inspiraenterprise-MBTA
Tracking with the useing mbta api

# Steps
1) create a any folder (e.g "inspiraenterprise:)
2) cd folder
3) virtualenv -p python3 env
4) clone project inside folder
5) source bin/activate
6) pip3 install -r requirements.txt
7) python foldername/manage.py runserver

#APIS
In these api ratelimit is applied, you cannot access more then 10 request in per min
Q1) API
1) Light Rail --> http://localhost:8000/subway/route/?type=0
2) Heavy Rail --> http://localhost:8000/subway/route/?type=1
3) Both heavy & Light Rail --> http://localhost:8000/subway/route/?type=0,1

Q2) API
1) subway route for more step --> http://localhost:8000/subway/stops/?type=0,1&route_stops=most
2) subway route for fewest step --> http://localhost:8000/subway/stops/?type=0,1&route_stops=fewest
3) A list of the stops that connect two or more subway routes along with the relevant
route names for each of those stops. --> http://localhost:8000/subway/stops/?type=0,1&route_stops=twoormore
