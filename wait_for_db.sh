#!/bin/sh 

echo "Waiting for postgres..."

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "PostgreSQL started"

# sleep for 2 seconds for the database to be ready to accept connections
sleep 2

# create tables and seed data to database
# TODO change this after adding alembic migrations
python bhagavad_gita_api/cli.py seed-data

# below line is to tell docker to continue the rest of the build flow
exec "$@"