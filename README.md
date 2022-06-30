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
output --> ![Screenshot from 2022-06-13 23-56-17](https://user-images.githubusercontent.com/30229429/173493882-6c97faf7-f653-464c-9769-42e0a18f3e41.png)
2) Heavy Rail --> http://localhost:8000/subway/route/?type=1
output --> ![Screenshot from 2022-06-13 23-56-24](https://user-images.githubusercontent.com/30229429/173493886-06790a8f-9881-46f7-a958-58c5bae2cc82.png)

3) Both heavy & Light Rail --> http://localhost:8000/subway/route/?type=0,1
output --> ![Screenshot from 2022-06-13 23-56-33](https://user-images.githubusercontent.com/30229429/173493887-e2e8a2bd-2e94-46a4-8880-61b09465c18c.png)

Q2) API
1) subway route for more step --> http://localhost:8000/subway/stops/?type=0,1&route_stops=most
output -- > ![Screenshot from 2022-06-14 10-16-12](https://user-images.githubusercontent.com/30229429/173495394-a2c1c6db-1df4-47f7-80c8-3bfdc3656520.png)
2) subway route for fewest step --> http://localhost:8000/subway/stops/?type=0,1&route_stops=fewest
output -- > ![Screenshot from 2022-06-14 10-18-15](https://user-images.githubusercontent.com/30229429/173495398-919268b7-7b26-4c44-b61a-bdf3b4c3bce4.png)
3) A list of the stops that connect two or more subway routes along with the relevant
route names for each of those stops. --> http://localhost:8000/subway/stops/?type=0,1&route_stops=twoormore
output --> ![Screenshot from 2022-06-13 23-57-35](https://user-images.githubusercontent.com/30229429/173493889-70b1990b-bb7d-451b-9ed6-39fe33f2966c.png)

![Screenshot from 2022-06-13 23-57-59](https://user-images.githubusercontent.com/30229429/173493890-3a3dd3b2-769d-40cc-b94c-729f713cdc6f.png)

![Screenshot from 2022-06-13 23-58-03](https://user-images.githubusercontent.com/30229429/173493895-d9677e44-b53d-4156-9e11-cac8d5c7e174.png)
