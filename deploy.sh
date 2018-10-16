#!/bin/bash
export HOST_IP=10.0.2.250
cd /home/ubuntu/microservice
docker-compose scale rootservice=0
docker rm $(docker ps -q -f status=exited)
docker rmi -f swiftops/pyjenkinsservice:latest && docker pull swiftops/pyjenkinsservice:latest && docker-compose up -d --remove-orphans