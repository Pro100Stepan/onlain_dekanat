#! /usr/bin/env sh

echo "Starting migrations:"
 
# Run migrations
echo "Start alembic"
#alembic revision --autogenerate -m "create account table"
echo "End alembic"

echo "Start upgrade head"
alembic upgrade head
echo "End upgrade head"
