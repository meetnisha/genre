#!/bin/sh
echo "\n"
echo "Stopping all running instances (if any) .. -->\n"
docker-compose down -v --remove-orphans

docker system prune