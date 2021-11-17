echo "Configuring config servers replica set ..."

docker exec -it mongocfg1 bash -c "echo 'rs.initiate({_id: \"mongors1conf\",configsvr: true, members: [{ _id : 0, host : \"mongocfg1\" },{ _id : 1, host : \"mongocfg2\" }, { _id : 2, host : \"mongocfg3\" }]})' | mongosh"
sleep 10
docker exec -it mongocfg1 bash -c "echo 'rs.status()' | mongosh"
sleep 10

echo "SUCCESSFULY CONFIGURED!"

echo "Shard1 replica set building ... "

docker exec -it mongors1n1 bash -c "echo 'rs.initiate({_id : \"mongors1\", members: [{ _id : 0, host : \"mongors1n1\" },{ _id : 1, host : \"mongors1n2\" },{ _id : 2, host : \"mongors1n3\" }]})' | mongosh"
sleep 10
docker exec -it mongors1n1 bash -c "echo 'rs.status()' | mongosh"
sleep 10
echo "Shard 1 built!"


echo "Shard2 replica set building ... "

docker exec -it mongors2n1 bash -c "echo 'rs.initiate({_id : \"mongors2\", members: [{ _id : 0, host : \"mongors2n1\" },{ _id : 1, host : \"mongors2n2\" },{ _id : 2, host : \"mongors2n3\" }]})' | mongosh"
sleep 10
docker exec -it mongors2n1 bash -c "echo 'rs.status()' | mongosh "
sleep 10
echo "Shard 2 built!"

echo "Introducing shards to the mongos router ..."

docker exec -it mongos1 bash -c "echo 'sh.addShard(\"mongors1/mongors1n1\")' | mongosh "
sleep 10
docker exec -it mongos1 bash -c "echo 'sh.addShard(\"mongors2/mongors2n1\")' | mongosh "
sleep 10
echo "Sharded mongo infra configured:"

docker exec -it mongos1 bash -c "echo 'sh.status()' | mongosh "
sleep 10
#containers=$(sudo docker ps | awk '{if(NR>1) print $NF}')
#for container in $containers
#do
#	echo "Container: $container"
#	if [[ $container == *"mongocfg"* ]]; then
#      echo "It's there!"
#    fi
#done