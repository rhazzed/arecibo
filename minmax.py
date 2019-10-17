import time
import sys

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure AZIMUTH servo
AZ=0
AZ_Min = 640  # 270 degrees ("artificial West")
AZ_Mid = 350  # 0 degrees ("artificial North")
AZ_Max =  75  # 90 degrees ("artificial East")

# Configure ELEVATION servo
EL=1
EL_Min = 665  # 0 degrees (pointing horizontally)
EL_Mid = 400  # 90 degrees (pointing vertically)
EL_Max = 195  # "beyond-vertically" (pointing > 95 degrees, or "wrapping around" behind us))

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



# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)


# Run full-range of motion test

while True:
    sDur=3

    try:
	pwm.set_pwm(AZ, 0, AZ_Mid)
	time.sleep(sDur)
	pwm.set_pwm(EL, 0, EL_Min)
	time.sleep(sDur)

	# Move servo on channel O between extremes.
	print("AZ MIN")
	pwm.set_pwm(AZ, 0, AZ_Min)
	time.sleep(sDur)
	print("AZ MAX")
	pwm.set_pwm(AZ, 0, AZ_Max)
	time.sleep(sDur)
	print("AZ MID")
	pwm.set_pwm(AZ, 0, AZ_Mid)
	time.sleep(sDur)
	print("EL MIN")
	pwm.set_pwm(EL, 0, EL_Min)
	time.sleep(sDur)
	print("EL MAX")
	pwm.set_pwm(EL, 0, EL_Max)
	time.sleep(sDur)
	print("EL MID")
	pwm.set_pwm(EL, 0, EL_Mid)
	time.sleep(sDur)
    except KeyboardInterrupt:
	# Center both servos and exit
	print("AZ MID")
    	pwm.set_pwm(AZ, 0, AZ_Mid)
	print("AZ MID")
    	pwm.set_pwm(EL, 0, EL_Mid)
	sys.exit(0)

