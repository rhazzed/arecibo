# arecibo
Autonomous Signal Tracker HOW-TO
=====================================

Buy a waveshare pan/tilt Pi Hat

Buy a directional antenna for 2.4 and 5 GHz WiFi, and mount it to your pan/tilt mount (pictures to follow...)
A very cheap, but workable antenna like this can be used -

* https://www.amazon.com/gp/product/B07SND1M93
* https://www.amazon.com/gp/product/B0781FHTT1
* https://www.banggood.com/1_35GHz-9_5GHz-UWB-Ultra-Wideband-Log-Periodic-Antenna-reviews-p1167608.html
* https://www.aliexpress.com/i/32815962974.html
* https://www.ebay.com/sch/i.html?_nkw=1.35GHz-9.5GHz+15W+UWB+Ultra+Wideband+Log+Periodic+Antenna+SMA+Connector
    

Install all of the following dependencies onto your Raspberry Pi -

    sudo apt-get install aircrack-ng pciutils tshark tcputils tcpdump Adafruit_Python_PCA9685
    sudo apt-get install wireshark (this one is optional)

Clone this github repository (arecibo) -

    git clone https://github.com/rhazzed/arecibo

Add a 2.4/5 GHz WiFi dongle to your Pi that has removable antennas, such as this EXCELLENT device (Panda Wireless PAU09 N600) -

* https://www.amazon.com/gp/product/B01LY35HGO

Attach your directional WiFi antenna (requires SMA Male) to one connector on the Panda adapter (requires RP-SMA Male), and either
remove the second antenna (not perfect) or add a 50-ohm termination to the other antenna connector (perfect).  You MUST remove the
second antenna, even if you don't terminate it.  (I bought a short SMA cable and a few SMA-to-RP-SMA adapters to connect the
antenna to the dongle.)

50 ohm SMA Male terminators -

* https://www.amazon.com/dp/B08CHFBTZ8

Stop Raspbian from trying to manage the Panda WiFi adapter by adding this to the end of /etc/dhcpcd.conf -

    denyinterfaces wlan1

Reboot after adding the above line to dhcpcd.conf

Create your own version of setup.conf.(whatever) and modify its values to match what it takes to properly rotate your
servos through their full range of motion (takes a bit of experimentation).

Symbolically link your version of setup.conf.(whatever) to setup.conf like this -

    ln -s setup.conf.(whatever) setup.conf

Run the doScan tool to identify the WiFi channel number and BSSID (MAC address) of the A.P. you want to locate -

    sudo ./doScan

Edit "doit" to tell it what WiFi channel and A.P. BSSID (MAC) address you want to locate
(HINT: Look for the "TO-DO:" lines near the top of the file)


Run "doit" as root via -

    sudo ./doit

Watch your pan/tilt assembly search for the give WiFi AP and point at it when it's done searching
