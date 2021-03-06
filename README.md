# eMotorWerks

##### Author: Sami Waheed
##### Date: August 2018

## Overview:
Access Historical Data For eMotorWerks Charging Stations Using the Juicenet API. 


## Description:
This program uses the Juicenet API to create a .csv file holding the historical data for the past 40 charging
sessions for an eMotorWerks charging station. It will either create a new .csv file or overwrite an existing one.
This only returns the history of 1 charging station, so this will need to be run and slightly altered for each
station accordinly. The areas that may need to be modified are clearly commented in the code. 'eMW_histData.py' is heavily commented
to allow for easy reuse. It also contains extra methods to access the Juicenet API. This was built off of @jesserockz repository, "python-juicenet." 


## Format of .csv File Created:
Timestamp, Power (Watts), Station ID

## To Use:
1. Jump to the 3 areas in 'eMW_hisData.py' labeled "*** Change Charger Index Accordingly Here". Change the Charger[] index to align with the correct station as needed.
2. Run 'runit.py'
3. The .csv file with the name specified will be created. You must close any files of the same name to successfully run the program


## Files:
1. eMW_histData.py # this contains the main program
2. runit.py        # driver program
3. init.py         
