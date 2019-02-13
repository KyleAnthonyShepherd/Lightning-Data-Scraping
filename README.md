# Lightning-Data-Scraping

This code pulls Lightning Strike data from National Interagency Fire Center (NIFC).<br/>
This data has Strike Location, Current (the Strength), and Polarity of the strike.<br/>
A bounding box in lat-long format is used to get the data of interest.<br/>
Real time data must be collected, because historical data is limited.<br/>
<br/>
If this script is run by itself, both functions are run using default values.<br/>
A bounding box of bbox=[30.167808,-95.958910,29.495183,-94.911649] is used.<br/>
Bulk data collection day is september 10th, 2018 (9,10,2018)<br/>
Real time data collection is used by getting system time and a 5 minute window.<br/>
<br/>
Function 1 is LightningDataBulk(day,bbox)<br/>
It collects data for an entire day (UTC time), for a provided day and bounding box.<br/>
Function 2 LightningDataRealTime(time,resolution,bbox)<br/>
It collects data for a time window resolution, for a given end time and bbox.<br/>
This script could be imported into another script, and the functions<br/>
LightningDataBulk(day,bbox)<br/>
LightningDataRealTime(time,resolution,bbox)<br/>
can be used on their own, if the imputs are provided.<br/>
<br/>
Data collected from here:<br/>
https://lightningapi.nifc.gov/viewer/<br/>
using the API:<br/>
https://lightningapi.nifc.gov/api/strike<br/>
and hijacking the authentication from the map service.<br/>
<br/>
Each Output file has variable data size.<br/>
However, each strike needs ~60 bytes of data to store.<br/>
A 200 GB hard drive can store ~3.3 billion lightning strikes.<br/>
<br/>
###<br/>
Code Written by:<br/>
Kyle Shepherd, at Rice University<br/>
kas20@rice.edu<br/>
Oct 24, 2018<br/>
###<br/>
