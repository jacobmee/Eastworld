#!/usr/bin/env bash

cd /home/pi/mjpg-streamer/
case "$1" in
    start)
        count=`pgrep mjpg_streamer | wc -l`
        if [ $count -eq 0 ]; then
            echo "Starting MJPG..."
            /home/pi/mjpg-streamer/mjpg_streamer -i "./input_raspicam.so" -o "./output_http.so -p 8000 -w ./www"
        else
            echo "MJPG already started"
        fi
        ;;
    stop)
        count=`pgrep mjpg_streamer | wc -l`
        if [ $count -eq 0 ]; then
            echo "MJPG didn't start yet"
        else
            echo "Killing MJPG"
            kill $(pgrep mjpg_streamer)
        fi
        ;;
    *)
        echo "Usage: start|stop"
        exit 1
        ;;
esac
exit 0