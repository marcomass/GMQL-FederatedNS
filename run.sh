#!/bin/bash

docker build . -t nameserver
( sleep 2; open http://localhost:8800/api/ ) &
( sleep 2; open http://localhost:8800/admin/ ) &
docker run -p 8800:8800 nameserver
