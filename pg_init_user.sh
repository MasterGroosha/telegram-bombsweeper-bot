#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER user;
    CREATE DATABASE sweeperdb;
    GRANT ALL PRIVILEGES ON DATABASE sweeperdb TO user;
EOSQL