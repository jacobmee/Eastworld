# Eastworld
This project is to re-create an "AI" world who can be useful helper.  With Raspberry came to alive, it becomes feasiable that small machines can talk to each other, enable other and interactive with humans.

The name comes from the TV series "West World", and hopefully with rapid development of robots in east world, we'll have more "AI" enable machines to help this planet.

Technical stack:
* Raspberry3 B+
* Python as main programming language
* Sensors:
    * Camera for facing recognition
    * Voice recognition (not enabled because the slowness, I'll try to enable Xunfei technology)
    * Text speaker from Baidu
    * Infrared detection for body and road blockers 
    * Motor wheels for movement
    * Ultrasonic for direction
* L298N chips for Raspberry extension
* 7.4V/6000mAh battery

  
## Setup
### Sports behavior
Default python libs is all enought, speicificly requires GPIO
### Watching behavior
#### 1. Imports mjpg for video streaming
    To be continued
### Dialog behavior
#### 1.Import audio listeners
    sudo apt-get install python-pyaudio python-pycurl FLAC
#### 1.A Config audio 
modifing "/etc/modprobe.d/alsa-base.conf
    
    # This sets the index value of the cards but doesn't reorder.
    options snd_usb_audio index=0
    options snd_bcm2835 index=1

    # Does the reordering.
    options snd slots=snd_usb_audio,snd_bcm2835

#### 1.B Test your audio card 
    arecord -d 10 -D plughw:0,0 test.wav
    aplay -D plughw:0,0 test.wav
#### 2. Import MP3 player
    sudo apt-get mpg123
#### 3. TTS tools 
    sudo pip install PyBaiduYuyin
    sudo pip install gTTS
#### 4. Speech Recognition
    pip install SpeechRecognition
    
### Load into system starts
    cp etc/eastworld /etc/init.d/
    sudo chmod +x /etc/init.d/eastworld
    sudo update-rc.d eastworld defaults
    sudo service eastworld start#启动
    sudo service eastworld stop#停止
