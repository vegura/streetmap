#!/usr/bin/env bash

docker exec -it c_mongo_1 bash -c "echo 'sh.enableSharding(\"taxi\")' | mongosh"
docker exec -it c_mongo_1 bash -c "echo 'sh.shardCollection(\"taxi.london_postcodes\", {\"_id\": \"hashed\"})' | mongosh"
