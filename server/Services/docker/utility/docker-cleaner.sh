#!/bin/sh

truncate -s 0 /var/lib/docker/containers/*/*-json.log
docker rmi `docker images | grep "^<none>" | awk "{print $3}"`
docker rmi `docker images -f "dangling=true" -q`
docker rm `docker ps -q -f status=exited`


