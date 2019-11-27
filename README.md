# arecibo
Autonomous Signal Tracker

Buy a waveshare pan/tilt Pi Hat

Buy a directional antenna for 2.4 and 5 GHz WiFi, and mount it to your pan/tilt mount (pictures to follow...)

Install all of the following dependencies onto your Raspberry Pi -
aircrack-ng
pciutils
tshark
tcputils
tcpdump
Adafruit_Python_PCA9685
wireshark (optional)

Clone this github repository (arecibo)

Add a Panda 2.4/5 GHz WiFi adapter to your Pi

Attach your directional WiFi antenna to one connector on the Panda adapter, and add a 50-ohm termination to the other Panda connector

Stop Raspbian from trying to manage the Panda WiFi adapter by adding this to the end of /etc/dhcpcd.conf -

    denyinterfaces wlan1

Reboot after adding the above line to dhcpcd.conf

Create your own version of setup.conf.(whatever) to setup.conf to match your servos

Symbolically link your version of setup.conf.(whatever) to setup.conf like this -

    ln -s setup.conf.(whatever) setup.conf

Edit "doit" to tell it what WiFi channel (1-11 on 2.4 GHz, 35-161 on 5 GHz) and A.P. MAC address you want to search for

Run the "doit" script as root via -

    sudo ./doit

Watch your pan/tilt assembly search for the give WiFi AP and point at it when it's done searching
