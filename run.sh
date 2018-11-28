#!/bin/bash

docker build . -t nameserver --build-arg db=../db.sqlite3

( sleep 2; open http://localhost:8800/api/ ) &
( sleep 2; open http://localhost:8800/admin/ ) &
docker run -p 8800:8800 nameserver
