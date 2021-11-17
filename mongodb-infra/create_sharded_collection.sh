docker exec -it mongors1n1 bash -c "echo 'use qqqq' | mongo"
sleep 10
docker exec -it mongos1 bash -c "echo 'sh.enableSharding(\"qqqq\")' | mongosh "
sleep 10
docker exec -it mongors1n1 bash -c "echo 'db.createCollection(\"qqqq.aaaa\")' | mongosh "
sleep 10
docker exec -it mongos1 bash -c "echo 'sh.shardCollection(\"qqqq.aaaa\", {\"name\" : 1})' | mongosh "
sleep 10