#!/bin/bash

set -e

# Replace myuser and mydb with your own values
# Don't forget to change them in .env file too!

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER myuser;
    CREATE DATABASE mydb;
    GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
EOSQL