#!/bin/bash
echo ""
echo "** GENRE CLASSIFICATION DEMO **"

echo ""
echo "Stopping previously running instances (if any) .. -->"
echo "---------------------------------------------------"
docker-compose down --remove-orphans
docker volume rm $(docker volume ls | awk '{print $2}')

echo "Run Tests -->"
echo "-----------------------------------------------------"
cd tests/
docker-compose up -d --build

#cd ../

echo
echo "Run Genre -->"
echo "-----------------------------------------------------"
docker-compose up -d core_api


echo
echo "All services are up and running...!!"
echo "-----------------------------------"
echo
echo "-----------------------------"
echo "Application is available at: "
echo "-----------------------------"
echo
echo "http://localhost:8000/"
echo
echo "-----------------------------"

