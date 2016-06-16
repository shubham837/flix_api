#!/bin/bash

sed -i 1d homework_segments.csv
sed -i 1d homework_route_segments.csv
sed -i 1d homework_rides.csv
sed -i 1d homework_tickets.csv

sed 's/\.0,/,/g' /tmp/homework_tickets.csv >> /tmp/homework_ticket.csv
rm /tmp/homework_tickets.csv

psql -d test_local_db -U postgres -c "COPY flb_segment(id, from_stop, destination_stop, distance) FROM '/tmp/homework_segments.csv' DELIMITER ',' CSV;"
psql -d test_local_db -U postgres -c "CREATE TABLE flb_routes_tmp(id INT,segment_id INT, sequence INT);"
psql -d test_local_db -U postgres -c "COPY flb_routes_tmp(id, segment_id, sequence) FROM '/tmp/homework_route_segments.csv' DELIMITER ',' CSV;"
psql -d test_local_db -U postgres -c "INSERT INTO flb_route(id) SELECT DISTINCT id FROM flb_routes_tmp"
psql -d test_local_db -U postgres -c "COPY flb_route_segment_mapping(route_id, segment_id, segment_sequence) FROM '/tmp/homework_route_segments.csv' DELIMITER ',' CSV;"
psql -d test_local_db -U postgres -c "COPY flb_ride(id, from_stop, destination_stop, route_id) FROM '/tmp/homework_rides.csv' DELIMITER ',' CSV;"
psql -d test_local_db -U postgres -c "CREATE TABLE flb_ticket_tmp (ride_id  int, from_stop int, destination_stop int, description varchar, transaction_hash varchar, price float, created_ts Date);"
psql -d test_local_db -U postgres -c "COPY flb_ticket_tmp(ride_id, from_stop, destination_stop, created_ts, description, transaction_hash, price) FROM '/tmp/homework_ticket.csv' DELIMITER ',' CSV;"
psql -d test_local_db -U postgres -c "INSERT INTO flb_ticket(ride_id, from_stop, destination_stop, created_ts, description, transaction_hash, price) SELECT ride_id, from_stop, destination_stop, created_ts, description,transaction_hash, price FROM flb_ticket_tmp WHERE EXISTS (SELECT 1 FROM flb_ride WHERE id = flb_ticket_tmp.ride_id);"
psql -d test_local_db -U postgres -c "INSERT INTO flb_ticket(ride_id, from_stop, destination_stop, created_ts, description, transaction_hash, price) SELECT null, from_stop, destination_stop, created_ts, description,transaction_hash, price FROM flb_ticket_tmp WHERE NOT EXISTS (SELECT 1 FROM flb_ride WHERE id = flb_ticket_tmp.ride_id);"
psql -d test_local_db -U postgres -c "DROP TABLE flb_routes_tmp"
psql -d test_local_db -U postgres -c "DROP TABLE flb_ticket_tmp"

