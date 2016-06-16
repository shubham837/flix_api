# FLIXBUS ASSIGNMENT
### Brief
This Application is based on the task defined here: https://gist.github.com/sash-ko/9a0b29db8d63c471860ee35c7a90f398
API Details are mentioned in following section:

Technologies Used in Application:<br/>
1) Docker<br/>
2) Programming Language: Python using Flask Framework<br/>
3) Backend Database: Postgres<br/>
4) Redis for Authentication storage<br/>
5) SQL Toolkit or ORM: SQLAlchemy<br/>
6) Marshmallow for serialization<br/>
7) Flake8 for maintaining code conventions<br/>
8) Supervisor for process Management<br/>
9) nose2 for test discovery<br/>

# Setup instructions

1) Prerequisites: You’ll need at least docker 1.10.<br/>

If you don’t already have it installed, follow the instructions for your OS:<br/>
a) On Mac OS X/Windows, you’ll need Docker Toolbox<br/>
b) On Linux, you’ll need docker-engine<br/>

2) Create the Machine:<br/>
a) docker-machine create --driver virtualbox default<br/>
b) eval $(docker-machine env default) # replace default with name of your docker machine<br/>

3) Build the Stack<br/>
a) docker-compose -f dev.yml build<br/>

4) Create Database Tables<br/>
a) docker-compose -f dev.yml run flask python manage.py syncdb<br/>

5) Copy CSV Data to postgres database:<br/>
a) Run script scripts/data_sync.sh with parameters defined in script<br/>
b) Usage: ./scripts/data_sync.sh ../flixbus_data/homework_segments.csv ../flixbus_data/homework_route_segments.csv ../flixbus_data/homework_rides.csv ../flixbus_data/homework_tickets.csv<br/>

5) Run the server<br/>
a) docker-compose -f dev.yml up<br/>

6) Check the ip where the server is running:<br/>
a) docker-machine ip default<br/>

# TestCase Run Instructions<br/>

1) docker-compose -f dev.yml run flask nose2 # runs all test cases<br/>
2) docker-compose -f dev.yml run flask nose2 test_promise # runs all test cases in test_segment_list_api.py<br/>


### Authentication<br/>
Application API's is protected using the authentication decorator.<br/>
'AUTH_KEY' and 'ACCESS_TOKEN' are stored and checked in redis for authenticating the user.<br/>

`APP_CLIENT` is used to identify a system. Send this across in headers to authorize internal calls.

# Segment API
Segment API is used to perform CRUD operations on segment resource:<br/>
1) Fetch list of segments: Returns list of segments in the system based on the query parameters.<br/>
API Endpoint: GET /segment?{query_parameters}<br/>
Allowed query_parameters:<br/>
get_pax Bool<br/>
get_revenue Bool<br/>
from_stop int<br/>
destination_stop int<br/>
distance int<br/>

## Example usage
###Request:
```
curl -X GET -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  http://192.168.99.100:5000/v1/segment?get_pax=true&get_revenue=false&from_stop=1
```

###Response:
```javascript
[{
"id": 1
"from_stop": 1,
"destination_stop": 10,
"distance": 5.3
"pax_count": 533
"revenue": 233
"currency": "EURO"
},
{
"id": 2
"from_stop": 1,
"destination_stop": 2,
"distance": 3.3
"pax_count": 53
"revenue": 234
"currency": "EURO"
}
]
```

2) POST a new segment<br/>
API Endpoint: POST /segment<br/>
## Example usage:
###Request:
```
curl -X POST -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  -d '{"from_stop":-11,"destination_stop":-2, "distance": 5.3}' http://192.168.99.100:5000/v1/segment
```

3) Get a specific Segment<br/>
API Endpoint: GET /segment/<segment_id>?{query_parameters}<br/>
Allowed query_parameters:<br/>
get_pax Bool<br/>
get_revenue Bool<br/>
from_stop int<br/>
destination_stop int<br/>
distance int<br/>

## Example usage:
###Request:
```
curl -X GET -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  http://192.168.99.100:5000/v1/segment/1?get_pax=true&get_revenue=false&from_stop=1
```

###Response:
```javascript
{
"id": 1
"from_stop": 1,
"destination_stop": 10,
"distance": 5.3
"pax_count": 533
"revenue": 233
"currency": "EURO"
}
```

4) UPDATE Existing segment<br/>
API Endpoint: PUT /segment/<segment_id><br/>
## Example usage:
###Request:
```
curl -X PUT -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  -d '{"from_stop":-11,"destination_stop":-2, "distance": 5.3}' http://192.168.99.100:5000/v1/segment/1
```

5) DELETE existing segment<br/>
API Endpoint: DELETE /segment/<segment_id><br/>
## Example usage:
###Request:
```
curl -X DELETE -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  http://192.168.99.100:5000/v1/segment/1?get_pax=true&get_revenue=false&from_stop=1
```

# Route API
Route API is used to perform CRUD operations on route resource:<br/>
1) Fetch list of routes: Returns list of routes in the system based on the query parameters.<br/>
API Endpoint: GET /route?{query_parameters}<br/>
Allowed query_parameters:<br/>
start int : offset<br/>
limit int : no. of results to be returned from offset<br/>
segment_id int: segment_id used for filtering<br/>

## Example usage:
###Request:
```
curl -X GET -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  http://192.168.99.100:5000/v1/route?start=0
```

###Response:
```javascript
[{
"id": 1
"segments": [
              {
                "segment_id": 1,
                "segment_sequence": 1
              },
              {
                "segment_id": 2,
                "segment_sequence": 2
              }
            ]
},
{
"id": 2
"segments": [
              {
                "segment_id": 3,
                "segment_sequence": 1
              },
              {
                "segment_id": 4,
                "segment_sequence": 2
              }
            ]
}
]
```

2) POST a new route<br/>
API Endpoint: POST /route<br/>

3) Get a specific Route<br/>
API Endpoint: GET /route/<route_id>?{query_parameters}<br/>
Allowed query_parameters:<br/>
Allowed query_parameters:<br/>
start int : offset<br/>
limit int : no. of results to be returned from offset<br/>
segment_id int: segment_id used for filtering<br/>

## Example usage:
###Request:
```
curl -X GET -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  http://192.168.99.100:5000/v1/route/1
```

###Response:
```javascript
{
"id": 1
"segments": [
              {
                "segment_id": 1,
                "segment_sequence": 1
              },
              {
                "segment_id": 2,
                "segment_sequence": 2
              }
            ]
}
```

4) UPDATE Existing segment<br/>
API Endpoint: PUT /segment/<segment_id><br/>


5) DELETE existing segment<br/>
API Endpoint: DELETE /segment/<segment_id><br/>
## Example usage:
###Request:
```
curl -X DELETE -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  http://192.168.99.100:5000/v1/segment/1?get_pax=true&get_revenue=false&from_stop=1
```

# Ride API
Ride API is used to perform CRUD operations on ride resource:<br/>
1) Fetch list of Ride: Returns list of rides in the system based on the query parameters.<br/>
API Endpoint: GET /route/<route_id>/ride?{query_parameters}<br/>
Allowed query_parameters:<br/>
from_stop int<br/>
destination_stop int<br/>

## Example usage:
###Request:
```
curl -X GET -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  http://192.168.99.100:5000/v1/route/1/ride
```

2) POST a new ride<br/>
API Endpoint: POST /route/<route_id>/ride<br/>


3) Get a specific Ride<br/>
API Endpoint: GET /route/<route_id>/ride/<ride_id>?{query_parameters}<br/>


4) UPDATE Existing ride<br/>
API Endpoint: PUT /route/<route_id>/ride/<ride_id><br/>


# Ticket API
Ticket API is used to perform CRUD operations on ticket resource:<br/>
1) Fetch list of tickets: Returns list of tickets in the system based on the query parameters.<br/>
API Endpoint: GET /ticket?{query_parameters}<br/>

2) POST a new ticket<br/>
API Endpoint: POST /ticket<br/>

3) Get a specific ticket <br/>
API Endpoint: GET /ticket/<ticket_id>?{query_parameters}<br/>

4) UPDATE Existing ticket<br/>
API Endpoint: PUT /ticket/<ticket_id><br/>


5) DELETE existing ticket<br/>
API Endpoint: DELETE /ticket/<ticket_id><br/>

