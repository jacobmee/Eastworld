cd /home/pi/mjpg-streamer
# Check if the process already exists.
count=`pgrep mjpg_streamer | wc -l`
if [ $count -eq 0 ]; then
echo "Starting mjpg..."
./mjpg_streamer -i "./input_raspicam.so" -o "./output_http.so -w ./www"
else
echo "mjpg already started, request ignored"
fi