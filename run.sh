#!/bin/bash

if [ -z "$1" ]
  then
   SRC=../target
  else
   SRC=$1
fi

echo "Database local folder: $(pwd)/$SRC"

if [ -z "$2" ]
  then
   PORT=8888
  else
   PORT=$2
fi

echo "Port: $PORT"

docker build . -t nameserver --build-arg db=/external/db.sqlite3

#( sleep 2; open http://localhost:8800/api/ ) &
#( sleep 2; open http://localhost:8800/admin/ ) &
docker run -p $PORT:8800 --mount type=bind,source="$(pwd)/$SRC",target=/external nameserver