export PGUSER=postgres
psql <<- EOSQL
    CREATE USER db_admin SUPERUSER;
    CREATE USER api_admin;
    CREATE DATABASE test_local_db;
EOSQL

