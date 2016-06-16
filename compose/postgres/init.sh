export PGUSER=postgres
psql <<- EOSQL
    CREATE USER db_admin SUPERUSER;
    CREATE USER api_admin;
    CREATE DATABASE test_local_db;
    #COPY flb_segment(id, from_stop, destination_stop, distance) FROM
    #'/tmp/homework_segments.csv' DELIMITER ',' CSV;
EOSQL

