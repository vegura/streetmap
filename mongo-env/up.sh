#!/usr/bin/env bash

mkdir data
export DATA_DIR=/home/vegura/Projects/university/streetmap/mongo-env/data

docker-compose -f config.yaml -f mongodb_network.yaml -f mongodb_shard1.yaml -f mongodb_shard2.yaml -f router.yaml up -d

# configuration of config servers replica-set
docker exec -it c_mongo_config_1 bash -c "echo 'rs.initiate({_id: \"mongo_rs1_config\",configsvr: true, members: [{ _id : 0, host : \"mongo_config_1\" },{ _id : 1, host : \"mongo_config_2\" }, { _id : 2, host : \"mongo_config_3\" }]})' | mongosh"

# checking status
docker exec -it c_mongo_config_1 bash -c "echo 'rs.status()' | mongosh"

# building shard replica set
# 1st shard
docker exec -it c_mongo_rs1_n1 bash -c "echo 'rs.initiate({_id : \"mongo_rs1\", members: [{ _id : 0, host : \"mongo_rs1_n1\" },{ _id : 1, host : \"mongo_rs1_n2\" },{ _id : 2, host : \"mongo_rs1_n3\" }]})' | mongosh"
# 2nd shard
docker exec -it c_mongo_rs2_n1 bash -c "echo 'rs.initiate({_id : \"mongo_rs2\", members: [{ _id : 0, host : \"mongo_rs2_n1\" },{ _id : 1, host : \"mongo_rs2_n2\" },{ _id : 2, host : \"mongo_rs2_n3\" }]})' | mongosh"

# again checking status
docker exec -it c_mongo_rs1_n1 bash -c "echo 'rs.status()' | mongosh"

# registering shards on routers
docker exec -it c_mongo_1 bash -c "echo 'sh.addShard(\"mongo_rs1/mongo_rs1_n1\")' | mongosh"
docker exec -it c_mongo_2 bash -c "echo 'sh.addShard(\"mongo_rs1/mongo_rs1_n1\")' | mongosh"

