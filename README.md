# FLIXBUS ASSIGNMENT
### Brief
This Application is based on the task defined here: https://gist.github.com/sash-ko/9a0b29db8d63c471860ee35c7a90f398
API Details are mentioned in following section:

Technologies Used in Application:
1) Docker
2) Programming Language: Python using Flask Framework
3) Backend Database: Postgres
4) Redis for Authentication storage
5) SQL Toolkit or ORM: SQLAlchemy
6) Marshmallow for serialization
7) Flake8 for maintaining code conventions
8) Supervisor for process Management
9) nose2 for test discovery

# Setup instructions

1) Prerequisites: You’ll need at least docker 1.10.

If you don’t already have it installed, follow the instructions for your OS:
    On Mac OS X/Windows, you’ll need Docker Toolbox
    On Linux, you’ll need docker-engine

2) Create the Machine:
    docker-machine create --driver virtualbox default
    eval $(docker-machine env default) # replace default with name of your docker machine

3) Build the Stack
    docker-compose -f dev.yml build

4) Create Database Tables
    docker-compose -f dev.yml run flask python manage.py syncdb

5) Copy CSV Data to postgres database:
    Run script {./scripts/data_sync.sh} with parameters defined in script
    Usage: ./scripts/data_sync.sh ../flixbus_data/homework_segments.csv ../flixbus_data/homework_route_segments.csv ../flixbus_data/homework_rides.csv ../flixbus_data/homework_tickets.csv

5) Run the server
    docker-compose -f dev.yml up

6) Check the ip where the server is running:
    docker-machine ip default

# TestCase Run Instructions

1) docker-compose -f dev.yml run flask nose2 # runs all test cases
2) docker-compose -f dev.yml run flask nose2 test_promise # runs all test cases in test_segment_list_api.py


### Authentication
Application API's is protected using the authentication decorator.
'AUTH_KEY' and 'ACCESS_TOKEN' are stored and checked in redis for authenticating the user.

`APP_CLIENT` is used to identify a system. Send this across in headers to authorize internal calls.

# Segment API
Segment API is used to perform CRUD operations on segment resource:
1) Fetch list of segments: Returns list of segments in the system based on the query parameters.
API Endpoint: GET /segment?{query_parameters}
Allowed query_parameters:
`
get_pax Bool
get_revenue Bool
from_stop int
destination_stop int
distance int
`
## Example usage:
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

2) POST a new segment
API Endpoint: POST /segment
## Example usage:
###Request:
```
curl -X POST -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  -d '{"from_stop":-11,"destination_stop":-2, "distance": 5.3}' http://192.168.99.100:5000/v1/segment
```

3) Get a specific Segment
API Endpoint: GET /segment/<segment_id>?{query_parameters}
Allowed query_parameters:
`
get_pax Bool
get_revenue Bool
from_stop int
destination_stop int
distance int
`
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

4) UPDATE Existing segment
API Endpoint: PUT /segment/<segment_id>
## Example usage:
###Request:
```
curl -X PUT -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  -d '{"from_stop":-11,"destination_stop":-2, "distance": 5.3}' http://192.168.99.100:5000/v1/segment/1
```

5) DELETE existing segment
API Endpoint: DELETE /segment/<segment_id>
## Example usage:
###Request:
```
curl -X DELETE -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  http://192.168.99.100:5000/v1/segment/1?get_pax=true&get_revenue=false&from_stop=1
```

# Route API
Route API is used to perform CRUD operations on route resource:
1) Fetch list of routes: Returns list of routes in the system based on the query parameters.
API Endpoint: GET /route?{query_parameters}
Allowed query_parameters:
`
start int : offset
limit int : no. of results to be returned from offset
segment_id int: segment_id used for filtering
`
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

2) POST a new route
API Endpoint: POST /route

3) Get a specific Route
API Endpoint: GET /route/<route_id>?{query_parameters}
Allowed query_parameters:
Allowed query_parameters:
`
start int : offset
limit int : no. of results to be returned from offset
segment_id int: segment_id used for filtering
`
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

4) UPDATE Existing segment
API Endpoint: PUT /segment/<segment_id>


5) DELETE existing segment
API Endpoint: DELETE /segment/<segment_id>
## Example usage:
###Request:
```
curl -X DELETE -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  http://192.168.99.100:5000/v1/segment/1?get_pax=true&get_revenue=false&from_stop=1
```

# Ride API
Ride API is used to perform CRUD operations on ride resource:
1) Fetch list of Ride: Returns list of rides in the system based on the query parameters.
API Endpoint: GET /route/<route_id>/ride?{query_parameters}
Allowed query_parameters:
`
from_stop int
destination_stop int
`
## Example usage:
###Request:
```
curl -X GET -H "Content-Type: application/json" -H "AUTH_KEY: AUTH_KEY1" -H "ACCESS_TOKEN: ACCESS_TOKEN_1" -H "APP_CLIENT: flixbus_data_app"  http://192.168.99.100:5000/v1/route/1/ride
```

2) POST a new ride
API Endpoint: POST /route/<route_id>/ride


3) Get a specific Ride
API Endpoint: GET /route/<route_id>/ride/<ride_id>?{query_parameters}


4) UPDATE Existing ride
API Endpoint: PUT /route/<route_id>/ride/<ride_id>


# Ticket API
Ticket API is used to perform CRUD operations on ticket resource:
1) Fetch list of tickets: Returns list of tickets in the system based on the query parameters.
API Endpoint: GET /ticket?{query_parameters}

2) POST a new ticket
API Endpoint: POST /ticket

3) Get a specific Segment
API Endpoint: GET /ticket/<ticket_id>?{query_parameters}

4) UPDATE Existing ticket
API Endpoint: PUT /ticket/<ticket_id>


5) DELETE existing ticket
API Endpoint: DELETE /ticket/<ticket_id>

