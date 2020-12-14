#!/bin/bash
app="flask-app"
docker build -t ${app} .
docker run -d -p 5000:80 --net my-net --name=${app} -v $PWD:/app ${app}