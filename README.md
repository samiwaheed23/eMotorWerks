# Access Historical Data For eMotorWerks Charging Stations Using the Juicenet API 
##### Author: Sami Waheed
##### Date: August 2018


This program uses the Juicenet API to create a .csv file holding the historical data for the past 40 charging
sessions for an eMotorWerks charging station. It will either create a new .csv file or overwrite an existing one.
This only returns the history of 1 charging station, so this will need to be run and slightly altered for each
station accordinly. The areas that may need to by modified are clearly commented in the code.


The format of the .csv file created is:

  timestamp | power (watts) | station ID
  __________|_______________|____________
            |               |
            |               |
            |               |
            |               |

TO USE:
-Jump to the 3 areas in "eMW_hisData.py" labeled "*** Change Charger Index Accordingly Here". Change the Charger[] index to align with the correct station as needed.
-Run runit.py
-.csv file with the name specified will be created. You must close any files of the same name to successfully run the program


