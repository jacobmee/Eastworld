#!/usr/bin/env bash

case "$1" in
    start)
        echo "Starting Music"
        mpc load fav
        mpc play
        ;;
    stop)
        echo "Stopping Music"
        mpc stop
        ;;
    *)
        echo "Usage: Music start|stop"
        exit 1
        ;;
esac
exit 0