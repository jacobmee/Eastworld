#!/bin/bash
service=emby-server

if (( $(ps -ef | grep -v grep | grep $service | wc -l) > 0 ))
then
        echo "$service is running!!!"
else
        echo "$service is starting!!!"
sudo service emby-server start
fi