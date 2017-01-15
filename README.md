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


### Sports behavior
Default python libs is all what needed, specifically GPIO
### Dialog behavior
##### 1. Import audio listeners
    sudo apt-get install python-pyaudio python-pycurl FLAC
##### 2. Test your audio card 
    arecord -d 10 -D plughw:0,0 test.wav
    aplay -D plughw:0,0 test.wav
##### 3. Import MP3 player
    sudo apt-get mpg123
##### 4. TTS tools 
    sudo pip install PyBaiduYuyin
    sudo pip install gTTS
##### 5. Speech Recognition
    sudo pip install SpeechRecognition
###### 5.1 PocketSphinx for local speech Recognition
    sudo apt-get install libpulse-dev
    sudo pip install pocketsphinx
    
Install all the SphinxBase build dependencies with 

    sudo apt-get install build-essential automake autotools-dev autoconf libtool.
Download and extract the SphinxBase source code.
Follow the instructions in the README to install SphinxBase. Basically, run 
    
    sh autogen.sh && ./configure && make && sudo make install
Goes to http://www.speech.cs.cmu.edu/tools/lmtool-new.html    
    
    # train your own words
    sphinx_lm_convert -i 0050.lm -o 0050.lm.bin
    sudo mv 0050.dic /usr/local/lib/python2.7/dist-packages/speech_recognition/pocketsphinx-data/en-US/pronounciation-dictionary.dict
    sudo mv 0050.lm.bin /usr/local/lib/python2.7/dist-packages/speech_recognition/pocketsphinx-data/en-US/language-model.lm.bin
##### 6. Load into system starts
    cp etc/raspcar /etc/init.d/
    sudo chmod +x /etc/init.d/raspcar
    sudo update-rc.d raspcar defaults
    sudo service raspcar start#启动
    sudo service raspcar stop#停止
### Smart Home behavior
This **Smart Home** can be connected with home devices, like camera, door, lights or anything devices enables openHAB.
    
    #Imports mjpg for video streaming
    #To be continued
##### 1. Installation
Add the **openHAB 2 Snapshot repositories** to your systems apt sources list:

    echo 'deb https://openhab.ci.cloudbees.com/job/openHAB-Distribution/ws/distributions/openhab-offline/target/apt-repo/ /' | sudo tee /etc/apt/sources.list.d/openhab2.list
    echo 'deb https://openhab.ci.cloudbees.com/job/openHAB-Distribution/ws/distributions/openhab-online/target/apt-repo/ /' | sudo tee --append /etc/apt/sources.list.d/openhab2.list

Additionally, you need to add the openHAB 2 Snapshots repository key to your package manager:
    
    wget -qO - 'http://www.openhab.org/keys/public-key-snapshots.asc' | sudo apt-key add -
Note: CloudBees provides the openHAB 2 repositories through HTTPS. If your system fails at the next step, install the missing dependency: 
    
    sudo apt-get install apt-transport-https

Scan the newly added repository and resynchronize the package index:

    sudo apt-get update
Finally install openHAB 2 as either offline or online distribution. **The offline distribution** is full blown and comes with all add-ons, **the online distribution** will install additional add-ons on request from the internet.

    sudo apt-get install openhab2-offline
    # or
    sudo apt-get install openhab2-online
    
##### 2. Configuration
Find the UUID and secrets

    UUID	/var/lib/openhab2/uuid
    Secret	/var/lib/openhab2/openhabcloud/secret

Make the user **openhab" has permission to initialize camera

    sudo usermod -a -G video openhab

##### 3. Upgrade JDK

    sudo tar zxvf jdk-8-linux-arm-vfp-hflt.tar.gz -C /opt

Set default java and javac to the new installed jdk8.
    
    $ sudo update-alternatives --install /usr/bin/javac javac /opt/jdk1.8.0/bin/javac 1
    $ sudo update-alternatives --install /usr/bin/java java /opt/jdk1.8.0/bin/java 1
    
    $ sudo update-alternatives --config javac
    $ sudo update-alternatives --config java
    
After all, verify with the commands with -verion option.
    
    $ java -version
    $ javac -version
    
### Camera behavior
Install opencv
    
    sudo apt-get install python-opencv