'''
This code pulls Lightning Strike data from National Interagency Fire Center (NIFC)
This data has Strike Location, Current (the Strength), and Polarity of the strike
A bounding box in lat-long format is used to get the data of interest
Real time data must be collected, because historical data is limited

If this script is run by itself, both functions are run using default values.
A bounding box of bbox=[30.167808,-95.958910,29.495183,-94.911649] is used.
Bulk data collection day is september 10th, 2018 (9,10,2018)
Real time data collection is used by getting system time and a 5 minute window

Function 1 is LightningDataBulk(day,bbox)
It collects data for an entire day (UTC time), for a provided day and bounding box
Function 2 LightningDataRealTime(time,resolution,bbox)
It collects data for a time window resolution, for a given end time and bbox
This script could be imported into another script, and the functions
LightningDataBulk(day,bbox)
LightningDataRealTime(time,resolution,bbox)
can be used on their own, if the imputs are provided

Data collected from here:
https://lightningapi.nifc.gov/viewer/
using the API:
https://lightningapi.nifc.gov/api/strike
and hijacking the authentication from the map service

Each Output file has variable data size
However, each strike needs ~60 bytes of data to store
A 200 GB hard drive can store ~3.3 billion lightning strikes

###
Code Written by:
Kyle Shepherd, at Rice University
kas20@rice.edu
Oct 24, 2018
###
'''
#### Import BLock ####
# the import block imports needed modules, and spits out a json file with
# version numbers so the code can be repeatable
file = open("LightningDataModuleVersions.json", 'w')
modules = {}

import os
import datetime

import sys
modules['Python'] = dict([('version', sys.version_info)])

import json
modules['json'] = dict([('version', json.__version__)])

import requests
modules['requests'] = dict([('version', requests.__version__)])

json.dump(modules, file, indent=4, sort_keys=True)
file.close()
#### END Import Block ####

def LightningDataBulk(day,bbox):
    '''
This function does the Bulk data import
It imports worldwide data within a given GMT (UTC) day
then data from outside of our area of interest is filtered away.

Inputs:
###
day: GMT Day to collect data
format: tuple. (Month,Day,Year)
Example:
day=(9,10,2018)

bbox:
defines the geographic bounding box to filter the data. Need the upper
left corner, and the lower right corner
Format:
list of 4 elements [lat UL, long UL, lat LR, long LR]
example:
[30.167808,-95.958910,29.495183,-94.911649]
###

The code outputs one file deliminated by |, with the lightning strike data
###
Headers:
Time of creation
Strike TimeStamp|Longitude|Latitude|Current|Polarity
###
'''
    if not os.path.exists('LightningData'):
        os.makedirs('LightningData') # creates data folder if it does not exist
    startTime='%02d/%02d/%04d 00:00:00' % day # creates strings for the URL
    endTime='%02d/%02d/%04d 23:59:59' % day
    # the request call. The server is kinda slow, so be patient
    r=requests.get('https://lightningapi.nifc.gov/api/strike?startTime='+startTime+'&endTime=' +endTime,auth=('lightning', 'Str!keD@ta'))
    text=r.json()
    f=open('LightningData/LightningData%04d-%02d-%02d' % (day[2],day[0],day[1]),'w')
    #header
    time=datetime.datetime.utcnow() # gets system time
    f.write('%04d-%02d-%02dT%02d%02d%02d\n' % (time.year,time.month,time.day,time.hour,time.minute,time.second))
    f.write('Strike TimeStamp|Longitude|Latitude|Current|Polarity\n')

    #loops over gathered lightning strikes
    for data in text["strikes"]:
        # only writes data if it is inside of the given bounding box
        if data['Longitude']<bbox[3] and data['Longitude']>bbox[1] and data['Latitude']>bbox[2] and data['Latitude']<bbox[0]:
            f.write(str(data['TimeStamp'])+'|'+str(data['Latitude'])+'|'+str(data['Longitude'])+'|'+str(data['Current'])+'|'+str(data['Polarity'])+'\n')



def LightningDataRealTime(time,resolution,bbox):
    '''
This function does the real time data import
It imports worldwide data between the given time (usually the current time),
and x minutes before the current time.
the data server uses GMT time (equal to UTC time)
Then data from outside of our area of interest is filtered away.

Inputs:
###
time: End time to collect data
format: datetime object
Example:
time = datetime.datetime.utcnow()

resolution: range of time to collect data, in minutes
format: integer
Example:
resolution=5

bbox:
defines the geographic bounding box to filter the data. Need the upper
left corner, and the lower right corner
Format:
list of 4 elements [lat UL, long UL, lat LR, long LR]
example:
[30.167808,-95.958910,29.495183,-94.911649]
###

The code outputs one file, with the lightning strike data
###
Headers:
Time of creation
Strike TimeStamp|Longitude|Latitude|Current|Polarity
###
'''
    if not os.path.exists('RealTimeLightningData'):
        os.makedirs('RealTimeLightningData') # creates data folder if it does not exist

    # creates strings for the URL
    Stime=time-datetime.timedelta(minutes=resolution)
    # startTime=str(Stime.month)+'/'+str(Stime.day)+'/'+str(Stime.year)+'%20'+str(Stime.hour)+':'+str(Stime.minute)+':'+str(Stime.second)
    # endTime=str(time.month)+'/'+str(time.day)+'/'+str(time.year)+'%20'+str(time.hour)+':'+str(time.minute)+':'+str(time.second)
    startTime='%02d/%02d/%04d %02d:%02d:%02d' % (Stime.month,Stime.day,Stime.year,Stime.hour,Stime.minute,Stime.second)
    endTime='%02d/%02d/%04d %02d:%02d:%02d' % (time.month,time.day,time.year,time.hour,time.minute,time.second)

    # the request call. The server is kinda slow, so be patient
    r=requests.get('https://lightningapi.nifc.gov/api/strike?startTime='+startTime+'&endTime=' +endTime,auth=('lightning', 'Str!keD@ta'))
    text=r.json()
    f=open('RealTimeLightningData/LightningData%04d-%02d-%02dT%02d%02d%02d' % (time.year,time.month,time.day,time.hour,time.minute,time.second),'w')
    #header
    f.write('%04d-%02d-%02dT%02d%02d%02d\n' % (time.year,time.month,time.day,time.hour,time.minute,time.second))
    f.write('Strike TimeStamp|Longitude|Latitude|Current|Polarity\n')
    #loops over gathered lightning strikes
    for data in text["strikes"]:
        # only writes data if it is inside of the given bounding box
        if data['Longitude']<bbox[3] and data['Longitude']>bbox[1] and data['Latitude']>bbox[2] and data['Latitude']<bbox[0]:
            f.write(str(data['TimeStamp'])+'|'+str(data['Latitude'])+'|'+str(data['Longitude'])+'|'+str(data['Current'])+'|'+str(data['Polarity'])+'\n')


if __name__ == "__main__":
    bbox=[30.167808,-95.958910,29.495183,-94.911649]
    day=(9,10,2018)
    time=datetime.datetime.utcnow()
    resolution=5
    print('Running bulk data collection for day '+str(day))
    LightningDataBulk(day,bbox)
    print('Running real time data collection for resolution '+str(resolution)+ ' minutes')
    LightningDataRealTime(time,resolution,bbox)
