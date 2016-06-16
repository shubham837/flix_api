#!/bin/bash
# Arguments {file_path for homework_segments.csv} {file_path for homework_route_segments.csv} {file_path for homework_rides.csv} {file_path for homework_tickets.csv}

docker cp scripts/store_csv_data_to_database.sh flixbus_postgres_1:/tmp/store_csv_data_to_database.sh
docker cp $1 flixbus_postgres_1:/tmp/homework_segments.csv
docker cp $2 flixbus_postgres_1:/tmp/homework_route_segments.csv
docker cp $3 flixbus_postgres_1:/tmp/homework_rides.csv
docker cp $4 flixbus_postgres_1:/tmp/homework_tickets.csv

docker exec -i -t flixbus_postgres_1 /bin/chmod 777 /tmp/store_csv_data_to_database.sh
docker exec -i -t flixbus_postgres_1 /tmp/store_csv_data_to_database.sh
