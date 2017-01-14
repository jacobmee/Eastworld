#!/usr/bin/env bash

case "$1" in
    start)
        echo "Starting Radio"
        mpc load radio
        mpc play
        ;;
    stop)
        echo "Stopping Radio"
        mpc stop
        ;;
    *)
        echo "Usage: Radio start|stop"
        exit 1
        ;;
esac
exit 0