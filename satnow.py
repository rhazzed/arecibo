#!/usr/bin/env python3
######################################################
# satnow.py - Calculate AZ, elevation and distance (in miles) between your QTH and one or more satellites RIGHT NOW
#
# HISTORICAL INFORMATION -
#
#  2022-03-07  KA9CQL msipin  Created from the current version of satdist.py
#  2022-03-08  KA9CQL msipin  Added satellite's current direction (rising/falling)
#                             Added display of next pass
#  2022-03-10  KA9CQL msipin  Display next-event time as 1st output field on the line to allow sorting by next event
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

def printHeading(sat,az,el,distance,indicator,t0,tz):
    # Display time/data
    tx_local = t0.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
    print(tx_local,"Local /",t0.utc_strftime('%Y-%m-%d %H:%M:%S'), "UTC", "-", end=' ')

    print("%-15s" % sat, end=indicator)

    #print("DEBUG: AZ - ",dir(az))
    print('  AZ: %3d' % int(az.degrees),end='')
    #print("DEBUG: EL - ",dir(el))
    print('   EL: %3d' % int(el.degrees),end='')
    print('   Dist: {:5.0f} mi'.format(distance.km * 0.621371),end=' ')



numargs = len(sys.argv)
if (numargs < 3):
    print("\nusage: %s <ground-station-gridsquare> <TLE-file_name_of_satellite_1> [ ... <TLE-file_name_of_satellite_n> ]\n" % sys.argv[0])
    sys.exit(1)

# This command is argument[0]

# Establish the minimum elevation
satarg=2
min_el = 12.0	# Default, unless specified on cmdline

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

# Establish time "a few seconds ago"
# Use 30-seconds (aka a half-a-minute) (0.5 of (24 hrs * 60 minutes))
ti_increment = (0.5/(24*60))
# Decrement time from "now"
t1 = t0 - ti_increment
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


    # Find az/el "a few seconds ago"
    topocentric = difference.at(t1)
    old_el, old_az, old_distance = topocentric.altaz()

    # Find az/el right now
    topocentric = difference.at(t0)
    now_el, now_az, now_distance = topocentric.altaz()
    print('\n\tDEBUG: now_EL: %3d' % int(now_el.degrees))


    # Develop indicator of satellite's motion
    indicator=' ? ' # Unknown
    if (now_el.degrees > old_el.degrees):
        indicator=' + ' # Rising
    if (now_el.degrees < old_el.degrees):
        indicator=' - ' # Falling
    if (now_el.degrees == old_el.degrees):
        indicator=' = ' # Stable


    # Identifies whether a successful pass was computed
    printed_heading=0

    # If satellite is currently above the horizon, print its heading (using the current time)
    if (now_el.degrees >= 0.0):
        printHeading(sat,now_az,now_el,now_distance,indicator,t0,tz)
        # Remember we've already printed this satellite's heading
        printed_heading = 1


    # Compute next pass
    ti_aos=t0
    ti_los=t0
    t, events = satellite.find_events(qth, t0, (t0 + 7), altitude_degrees=0.9)
    for ti, event in zip(t, events):
        # Find az/el at this event
        topocentric = difference.at(ti)
        el, az, distance = topocentric.altaz()

        # AOS = acquisition of signal, MAX = maximum elevation, LOS = loss of signal
        name = ('AOS', 'MAX', 'LOS')[event]

        tx_local = ti.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
        mins = int((ti - t0)*(24*60))
        hrs = int(mins/60.0)
        mins = (mins - (hrs*60))

        if (name == "AOS"):
            ti_aos = ti

            #print(" | Next AOS - ",tx_local,"/",ti.utc_strftime('%Y-%m-%d %H:%M:%S'), "UTC", "-", end=' ')
            #print(tx_local,"/",ti.utc_strftime('%Y-%m-%d %H:%M:%S'), "UTC", "- AOS -", end=' ')
            #print(" | Next AOS - ",tx_local, end=' ')
            #print(" | Next AOS - ",int((ti - t0)*(24*60)),"mins", end=' ')
            if (printed_heading == 0):
                printHeading(sat,now_az,now_el,now_distance,indicator,ti_aos,tz)
                printed_heading = 1

            print("| AOS in",end=' ')
            if (hrs > 0):
                print("%dh" % hrs,end=' ')
            if (mins >= 1.0):
                print("%dm" % mins, end=' ')
            else:
                print("%ds" % int(mins * 60), end=' ')

        if (name == "MAX"):
            print('| MAX %d deg' % int(el.degrees),end=' ')
            #print(tx_local,"/",ti.utc_strftime('%Y-%m-%d %H:%M:%S'), "UTC", "-", end=' ')
            #print(tx_local, end=' ')

        if (name == "LOS"):
            ti_los = ti
            mins = int((ti_los - ti_aos)*(24*60))
            hrs = int(mins/60.0)
            mins = (mins - (hrs*60))
            #print(" | Next LOS - ",tx_local,"/",ti.utc_strftime('%Y-%m-%d %H:%M:%S'), "UTC")
            #print("| LOS:",tx_local)
            #print("| LOS after",end=' ')
            print("|",end=' ')
            if (hrs > 0):
                print("%d hr" % hrs,end=' ')
            if (mins >= 1.0):
                print("%d min" % mins, end=' ')
            else:
                print("%d sec" % int(mins * 60), end=' ')
            print("pass",end='')
            break

    # If this satellite didn't cross our sky (as indicated by NO-AOS-FOUND) then display where
    # it currently is, anyway
    if (printed_heading == 0):
        printHeading(sat,now_az,now_el,now_distance,indicator,t0,tz)
        printed_heading = 1

    print("")










print()
sys.exit(0)

