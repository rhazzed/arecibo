#!/usr/bin/env python3
######################################################
# satdist.py - Calculate AZ, elevation and distance (in miles) between your QTH and one or more satellites
#
# HISTORICAL INFORMATION -
#
#  2022-02-27  msipin  Created from the current version of gsdist.py
#  2022-03-03  msipin  Initialized times using skyfield datatype, rather than Unix datetimes.
#  2022-03-07  msipin  If user specified a lower minimum "workable" elevation than our first-pass orbit-check
#                      elevation, use their value on first-pass oribit checks.
######################################################
# You need to install this Python3 library -
#       sudo pip3 install skyfield

from skyfield.api import Topos, load, wgs84
import datetime
from datetime import timezone
from dateutil import tz
import sys




def DegreesToRadians(tDegrees):
 return ((float(tDegrees) * math.pi) / 180.0)

def RadiansToDegrees(tRadians):
 return ((float(tRadians) * 180.0) / math.pi)

def RadiansToNaticalMiles(tRadians):
 return ((float(tRadians) * 10800.0 ) / math.pi) # 10800 = 180 * 60

def NaticalMilesToStatueMiles(tNaticalMiles):
 return (float(tNaticalMiles) * 1.15)

def StatuteMilesToNaticalMiles(tStatueMiles):
 return (float(tStatueMiles) / 1.15)

def StatuteMilesToKilometers(tStatueMiles):
 return (float(tStatueMiles) * 1.609344)


#stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
#satellite = by_name['ISS (ZARYA)']
stations_url = "https://www.amsat.org/tle/current/nasabare.txt"
#satellite = by_name['AO-07']

satellites = load.tle_file(stations_url)
print('Loaded', len(satellites), 'satellites')


ts = load.timescale(builtin=True)

def gridCase(input):
    A=''
    B=''
    C=''
    D=''
    E=''
    F=''

    if (len(input)>= 4):
        chars = [char for char in input]  
        A=chars[0].upper()  # Long
        B=chars[1].upper()  # Latt
        C=chars[2]  # Long
        D=chars[3]  # Latt
        if (len(input)>= 6):
            E=chars[4].lower()  # Long
            F=chars[5].lower()  # Latt
    if ((A >= 'A') and (A <= 'R') and (B >= 'A') and (B <= 'R')):
        return(A+B+C+D+E+F)
    return('?')



def gs2LatLon(input):
    lat=0.0
    lon=0.0
    if (len(input)>= 4):
        chars = [char for char in input]  
        A=chars[0]  # Long
        B=chars[1]  # Latt
        C=chars[2]  # Long
        D=chars[3]  # Latt
        if (len(input)>= 6):
            E=chars[4]  # Long
            F=chars[5]  # Latt
            lon=getLon3(A,C,E)
            lat=getLat3(B,D,F)
        else:
            lon=getLon2(A,C)
            lat=getLat2(B,D)
    return(lat,lon)



def getLon2(LoA,LoB):
    return getLon3(LoA,LoB,'l')


def getLon3(LoA,LoB,LoC):
    a=ord(LoA) - ord('A')	# A - R (18 possibilities) 'I'/'J' = mid
    a=a*20			# 20 degrees Lon each
    b=ord(LoB) - ord('0')	# 0 - 9 (10 possibilities) '4'/'5' = mid
    b=b*2			# 2 degrees Lon each
    c=ord(LoC) - ord('a')	# a - x (24 possibilities) 'l'/'m' = mid
    #c=(c*5)/60			# 5 minutes Lon each
    c=(c/12)+(1/24)		# FROM WEBSITE - ISN'T EXPLAINED
    Lon=a+b+c-180.0
    #print("Longitude: ", Lon)
    return Lon


def getLat2(LaA,LaB):
    return getLat3(LaA,LaB,'l')


def getLat3(LaA,LaB,LaC):
    d=ord(LaA) - ord('A')
    d=d*10			# 10 degrees Lat each
    e=ord(LaB) - ord('0')
    e=e*1			# 1 degree Lat each (no adjustment needed)
    f=ord(LaC) - ord('a')
    #f=(f*2.5)/60		# 2.5 minutes Lat each
    f=(f/24)+(1/48)		# FROM WEBSITE - ISN'T EXPLAINED
    Lat=d+e+f-90.0
    #print("Latitude: ",Lat)
    return Lat




numargs = len(sys.argv)
if (numargs < 3):
    print("\nusage: %s [ -m minimun_elevation_in_degrees ] <ground-station-gridsquare> <TLE-file_name_of_satellite_1> [ ... <TLE-file_name_of_satellite_n> ]\n" % sys.argv[0])
    sys.exit(1)

# This command is argument[0]

# Elevation to check on first pass should be "fairly low"
first_check_min_el=10.0

# Establish the minimum "workable" elevation
satarg=2
min_el = 12.0	# Default, unless specified on cmdline
# See if user wants to override the minimum "workable" elevation
if (numargs >= 5):
    ##print("DEBUG: enough args")
    if (sys.argv[1] == "-m"):
        ##print("DEBUG: matches '-m'")
        min_el = float(sys.argv[2])
        ##print("DEBUG: New min_el = ",min_el)
        satarg = satarg + 2

# If user specified a minimum "workable" elevation lower than our first_check_min_el, use that as our first check value
if min_el < first_check_min_el:
    first_check_min_el = min_el

# Gridsquare is argument[satarg-1]
# DM14
#Pos1="DM14hl"
Pos1=gridCase(sys.argv[satarg-1])

print("Pos: ",gridCase(Pos1))



Lat1=0.0
Lon1=0.0
if (len(Pos1) >= 4):
    ##print("\n")
    Lat1,Lon1 = gs2LatLon(Pos1)

print("Longitude1: ", Lon1)
ew1='E'
if (Lon1 < 0.0):
    ew1='W'
    ##Lon1 = Lon1 * (-1.000)
print("E/W: ", ew1)

print("Latitude1: ", Lat1)
ns1='N'
if (Lat1 < 0.0):
    ns1='S'
    ##Lat1 = Lat1 * (-1.000)
print("N/S: ", ns1)
print("")

# Start time (now) -
now = datetime.datetime.now(timezone.utc)
t0 = ts.utc(now)
##print(t0)
# Run passes for the next 24 hours (1 day)
t1 = t0 + 1
##print(t1)

# Get local timezone
tz = tz.tzlocal()


print("Current time:",t0.utc_strftime('%Y-%m-%d %H:%M:%S'), "UTC")
tilocal = t0.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
print("Current time:",tilocal,"Local")
print()

qth = wgs84.latlon(Lat1, Lon1)

# Satellite name(s) are arguments[2+]
for i in range(satarg,numargs):
    sat = sys.argv[i]
    ##print("\nSat: ",sat)

    by_name = {sat.name: sat for sat in satellites}
    #satellite = by_name['ISS (ZARYA)']
    satellite = by_name[sat]
    ##print(satellite)

    difference = satellite - qth


    # Figure out when the satellite is passing above the horizon (aka "elevation") "at least a little bit" (above maybe 10 degrees?)
    ##print("\n++++", satellite)
    t, events = satellite.find_events(qth, t0, t1, altitude_degrees=first_check_min_el)
    good_pass = 0
    t_aos=t1
    t_max=t1
    t_los=t1
    for ti, event in zip(t, events):

        # Find az/el at this event
        topocentric = difference.at(ti)
        el, az, distance = topocentric.altaz()

        # AOS = acquisition of signal, MAX = maximum elevation, LOS = loss of signal
        name = ('AOS', 'MAX', 'LOS')[event]

        if (name == "AOS"):
            #print("^^^^  CQ  ^^^^  CQ  ^^^^  CQ  ^^^^  CQ  ^^^^  CQ  ^^^^  CQ ^^^^") 
            #print('   EL: %3d' % int(el.degrees),end='\n')
            t_aos = ti
            good_pass = 0

        if (name == "MAX"):
            #print("++++      ++++      ++++      ++++      ++++      ++++     ++++") 
            #print('   EL: %3d' % int(el.degrees),end='\n')
            if float(el.degrees) >= min_el:
                good_pass = 1
                #print('   DEBUG: GOOD PASS!')
                t_max = ti

        if (name == "LOS"):
            #print("----  73  ----  73  ----  73  ----  73  ----  73  ----  73 ----") 
            #print('   EL: %3d' % int(el.degrees),end='\n')
            t_los = ti



            if good_pass == 1:
                #print('   DEBUG: GOOD PASS!')
                # Produce detailed track of this satellite over time

                # Use one-minute increments (1 of (24 hrs * 60 minutes))
                ti_increment = (1/(24*60))

                tx = t_aos

                # Loop until tx exceeds t_los
                name = "AOS"
                while (t_los - tx) > 0:

                    # Compute azel at tx
                    topocentric = difference.at(tx)
                    el, az, distance = topocentric.altaz()

                    # Display time/data
                    tx_local = tx.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
                    print(tx_local,"Local /",tx.utc_strftime('%Y-%m-%d %H:%M:%S'), "UTC", "-", end=' ')
                    print("%-15s" % sat, end=' - ')

                    # See if incrementing tx would cross the t_max threshold - if so, increment tx directly to t_max
                    if ((t_max - tx) > 0) and ((t_max - (tx + ti_increment)) < 0):
                        tx = t_max
                        print(name, end=' ')
                        name = "MAX"
                    else:
                        if (t_max - tx) == 0.0:
                            name = "MAX"

                        # Increment time
                        tx = tx + ti_increment

                        if (t_los - tx) < 0:
                            name = "LOS"

                        print(name, end=' ')

                    name = "   "

                    #print("DEBUG: AZ - ",dir(az))
                    print('  AZ: %3d' % int(az.degrees),end='')
                    #print("DEBUG: EL - ",dir(el))
                    print('   EL: %3d' % int(el.degrees),end='')
                    print('   Dist: {:5.0f} mi'.format(distance.km * 0.621371))



sys.exit(0)

