#!/usr/bin/env bash

case "$1" in
    leave.home)
        echo "leave home actions"
        sh /home/pi/Eastworld/etc/mjpg.sh start
        ;;
    back.home)
        echo "back home actions"
        sh /home/pi/Eastworld/etc/mjpg.sh stop
        ;;
    *)
        echo "Usage: leave.home| back.home"
        exit 1
        ;;
esac
exit 0