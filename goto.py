###########################
# goto.py - Slew the pan/tilt adapter to the given azimuth/elevation pairing specified by the command line
#
# HISTORICAL INFORMATION -
#
#  2019-11-18  msipin  Created from minmax.py
###########################

import time
import sys

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

try:
    import configparser
except ImportError:
    print("\nERROR: Can't find 'configparser'.  Try performing 'sudo pip install ConfigParser'\n")
    sys.exit(-1)




# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)



## setup.conf contents -
## [pan_tilt_servos]
## name1 = value1
Config = configparser.ConfigParser()
Config.read("setup.conf")

section="panTiltServos"

AZ = int(Config.get(section, 'az'))
AZ_Min = int(Config.get(section, 'az_min'))
AZ_Mid = int(Config.get(section, 'az_mid'))
AZ_Max = int(Config.get(section, 'az_max'))

EL = int(Config.get(section, 'el'))
EL_Min = int(Config.get(section, 'el_min'))
EL_Mid = int(Config.get(section, 'el_mid'))
EL_Max = int(Config.get(section, 'el_max'))


PWMs_PER_DEG_AZ = abs(AZ_Min - AZ_Max)/180.0

PWMs_PER_DEG_EL = abs(EL_Min - EL_Mid)/90.0


# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)




# Move ELEVATION servo to the given location (0 is EL_Min, 90 is EL_Mid)
def gotoEL(el_deg):

	# Constrain input to 0 <= x <= 90
	if (el_deg < 0):
		el_deg = 0
	if (el_deg > 90):
		el_deg = 90

	try:
		# Move ELEVATION servo to the given location
		print("Moving EL to: %d" % el_deg)
		loc = el_deg		# Don't need an offset
		if (EL_Min > EL_Mid):
			# Subtract from EL_Min
			new_loc = int(EL_Min - (loc * PWMs_PER_DEG_EL))
			# Don't let new setting go below EL_Mid
			if (new_loc < EL_Mid):
				new_loc = EL_Mid
		else:
			# Add to EL_Min
			new_loc = int(EL_Min + (loc * PWMs_PER_DEG_EL))
			# Don't let new setting go above EL_Mid
			if (new_loc > EL_Mid):
				new_loc = EL_Mid

		print("Setting PWM to: %d\n" % new_loc)
		pwm.set_pwm(EL, 0, new_loc)

	except KeyboardInterrupt:
		# Center ELEVATION and exit
		print("EL MID")
    		pwm.set_pwm(EL, 0, EL_Mid)
		sys.exit(0)




# Move AZIMUTH servo to the given location (-90 is "West", 0 is "North", +90 is "East")
def gotoAZ(az_deg):

	# Constrain input to -90 <= x <= +90
	if (az_deg < -90):
		az_deg = -90
	if (az_deg > 90):
		az_deg = 90

	try:
		# Move AZIMUTH servo to the given location
		print("Moving AZ to: %d" % az_deg)
		loc = az_deg + 90	# Offset input value where 0 = West, 90 = North, 180 = East
		if (AZ_Min > AZ_Max):
			# Subtract from AZ_Min
			new_loc = int(AZ_Min - (loc * PWMs_PER_DEG_AZ))
			# Don't let new setting go below AZ_Max
			if (new_loc < AZ_Max):
				new_loc = AZ_Max
		else:
			# Add to AZ_Min
			new_loc = int(AZ_Min + (loc * PWMs_PER_DEG_AZ))
			# Don't let new setting go above AZ_Max
			if (new_loc > AZ_Max):
				new_loc = AZ_Max

		print("Setting PWM to: %d\n" % new_loc)
		pwm.set_pwm(AZ, 0, new_loc)

	except KeyboardInterrupt:
		# Center AZIMUTH and exit
		print("AZ MID")
    		pwm.set_pwm(AZ, 0, AZ_Mid)
		sys.exit(0)





def RunSteppedElevation():
	sDur=0.10
	# Run stepped-elevation test

	pwm.set_pwm(AZ, 0, AZ_Mid)
	time.sleep(2)
	pwm.set_pwm(EL, 0, EL_Min)
	print("EL at %d" % EL_Min)
	time.sleep(2)

	while True:

	    try:

		# Move Elevation servo from horizontal to vertical in steps
		for i in range(1, 20):
			val = (EL_Min-10) - (((EL_Min  - (EL_Mid+5))/90)*(i*5))
			pwm.set_pwm(EL, 0, val)
			print("EL at %d" % val)
			time.sleep(sDur)
		for i in range(0, 19):
			val = EL_Mid + (((EL_Min  - (EL_Mid+5))/90)*(i*5))
			pwm.set_pwm(EL, 0, val)
			print("EL at %d" % val)
			time.sleep(sDur)
	    except KeyboardInterrupt:
		# Center both servos and exit
		print("AZ MID")
    		pwm.set_pwm(AZ, 0, AZ_Mid)
		print("EL MAX")
    		pwm.set_pwm(EL, 0, EL_Max)
		time.sleep(1)
		print("EL MID")
    		pwm.set_pwm(EL, 0, EL_Mid)
		sys.exit(0)



def RunGotoAz():
	sDur=0.2

	# Go to -90 azimuth
	gotoAZ(-90)
	time.sleep(sDur)

	# Go to -45 azimuth
	gotoAZ(-45)
	time.sleep(sDur)

	# Go to 0 azimuth
	gotoAZ(0)
	time.sleep(sDur)

	# Go to +45 azimuth
	gotoAZ(45)
	time.sleep(sDur)

	# Go to +90 azimuth
	gotoAZ(90)
	time.sleep(sDur)

	# Got to AZ_Mid
	gotoAZ(0)
	time.sleep(sDur)



def RunGotoEl():
	sDur=0.1

	# Go to 0 Elevation
	gotoEL(0)
	time.sleep(sDur)

	# Go to 15 Elevation
	gotoEL(15)
	time.sleep(sDur)

	# Go to 30 Elevation
	gotoEL(30)
	time.sleep(sDur)

	# Go to 45 Elevation
	gotoEL(45)
	time.sleep(sDur)

	# Go to 60 Elevation
	gotoEL(60)
	time.sleep(sDur)

	# Go to 75 Elevation
	gotoEL(75)
	time.sleep(sDur)

	# Go to 90 Elevation
	gotoEL(90)
	time.sleep(sDur)




def RunDiagonal():
    sDur=0.020
    az=0
    el=90
    stepDeg=-0.5

    gotoAZ(az)
    gotoEL(el)
    time.sleep(2)

    try:

	for i in range(0,int(90/abs(stepDeg))):
		gotoAZ(az + (i * stepDeg))
		gotoEL(el + (i * stepDeg))
		time.sleep(sDur)

	RunGotoEl()
	RunGotoAz()

    except KeyboardInterrupt:
	# Center both servos and exit
	print("AZ MID")
	pwm.set_pwm(AZ, 0, AZ_Mid)
	print("EL MID")
	pwm.set_pwm(EL, 0, EL_Mid)
	sys.exit(0)




# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

##RunFullAZ()

##RunFullEL()

##RunFullMotion()

##RunSteppedElevation()

##RunSteppedAzimuth()

##RunGotoAz()

##RunGotoEl()

RunDiagonal()
