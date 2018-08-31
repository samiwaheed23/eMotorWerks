#   This program uses the Juicenet API to create a .csv file holding the historical data for the past 40 charging
#   sessions for a eMotorWerks charging station. It will either create a new .csv file or overwrite an existing one.
#   This only returns the history of 1 charging station, so this will need to be run and slightly altered for each
#   station. The areas that may need to be modified are clearly commented in the code.
#
#
#   The format of the file is:
#
#       timestamp | power (watts) | station ID
#       __________|_______________|____________
#                 |               |
#                 |               |
#                 |               |
#                 |               |
#   TO USE:
#   -Jump to the 3 areas labeled "*** Change Charger Index Accordingly Here ***". Change the Charger[] index to
#   align with the correct station as needed.
#   -Run runit.py
#   -.csv file with the name specified will be created. You must close any files of the same name to successfully
#   run the program
#
#

import uuid
import json
import time
import requests
import csv

class eMW_histData:

    def __init__(self):
        pass

    def run(self):

        # Access Juicenet API
        # Enter API credentials here
        zappers = Api('')
        chargers = zappers.get_devices()

        Tokens = [c.token() for c in chargers]

        # Get Dictionary of Charging History
        # *** Change Charger Index Accordingly Here ***
        chargingHist = zappers.get_history(chargers[ ])
        # ***                                       ***

        del chargingHist['success']
        del chargingHist['continuity_token']

        # Build List of All Session IDs
        sessionIDs = []
        for s in chargingHist['sessions']:
            sessionIDs.append(s['id'])
        print (sessionIDs)
        print ("")


        # Build List of Dictionaries for (time, power, session ID)
        finalList = []
        for i in range(0, len(sessionIDs)):

            # *** Change Charger Index Accordingly Here ***
            tempPlot = zappers.get_plot(chargers[ ], sessionIDs[i])
            # ***                                       ***

            # Cleans Dictionary
            del tempPlot['success']
            # print (sessionIDs[i])
            # print (tempPlot)

            # Save Length of List Before Extending it
            oldCount = len(finalList)

            for j in range(0, len(tempPlot['points'])):
                finalList.append(tempPlot['points'][j])

            # Adds ID to Each Dictionary
            for j in range(oldCount, len(finalList)):
                finalList[j]["id"] = sessionIDs[i]

        # Write to .csv File
        # *** Change File Name Accordingly Here ***
        with open('history_station.csv', 'w') as resultFile:
        # ***                                       ***

            fieldnames = ['t', 'v', 'id']
            wr = csv.DictWriter(resultFile, dialect= 'excel', quoting=csv.QUOTE_ALL, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
            wr.writerows(finalList)

        resultFile.close()

# ---------------------------------------------------------------------------------

class Api:

    BASE_URL = "http://emwjuicebox.cloudapp.net"

    def __init__(self, api_token):
        self.api_token = api_token
        self.uuid = str(uuid.uuid4())

    def get_devices(self):
        data = {
            "device_id": self.uuid,
            "cmd": "get_account_units",
            "account_token": self.api_token
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post("{}/box_pin".format(self.BASE_URL),
                                 data=json.dumps(data),
                                 headers=headers)
        response_json = response.json()
        units_json = response_json.get("units")
        devices = []
        for unit in units_json:
            device = Charger(unit, self)
            device.update_state()
            devices.append(device)

        return devices

    # Returns state of device (plugged, charging, standby, disconnected)
    def get_device_state(self, charger):
        data = {
            "device_id": self.uuid,
            "cmd": "get_state",
            "token": charger.token(),
            "account_token": self.api_token
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post("{}/box_api_secure".format(self.BASE_URL),
                                 data=json.dumps(data),
                                 headers=headers)
        response_json = response.json()
        return response_json

    # Returns session IDs of last 40 sessions per charging station
    def get_history(self, charger):
        data = {
            "device_id": self.uuid,
            "cmd": "get_history",
            "token": charger.token(),
            "account_token": self.api_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post("{}/box_api_secure".format(self.BASE_URL),
                                 data=json.dumps(data),
                                 headers=headers)
        response_json = response.json()
        return response_json

    # Returns a timestamp and power (watts) for a single session ID and associated charging station
    def get_plot(self, charger, sessionID):
        data = {
            "cmd": "get_plot",
            "device_id": self.uuid,
            "token": charger.token(),
            "account_token": self.api_token,
            "attribute": "power",
            "intervals": 100,               # Can change this number 
            "session_id": sessionID
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post("{}/box_api_secure".format(self.BASE_URL),
                                 data=json.dumps(data),
                                 headers=headers)
        response_json = response.json()
        return response_json

    # Sends Setpoint Amps of Current to Charger Station
    def set_max_amperage(self, setpoint, charger):
            data = {
                "device_id": self.uuid,
                "cmd": "set_limit",
                "token": charger.token(),
                "amperage": setpoint
            }
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post("{}/box_api_secure".format(self.BASE_URL),
                                 data=json.dumps(data),
                                 headers=headers)
            #response_json = response.json()
            #return response_json

# ---------------------------------------------------------------------------------

class Charger:
    def __init__(self, json_settings, api):
        self.json_settings = json_settings
        self.json_state = {}
        self.api = api
        self.last_updated_at = 0

    def name(self):
        return self.json_settings.get("name")

    def token(self):
        return self.json_settings.get("token")

    def id(self):
        return self.json_settings.get("unit_id")

    def update_state(self):
        """ Update state with latest info from API. """
        if time.time() - self.last_updated_at < 30:
            return True
        self.last_updated_at = time.time()
        json_state = self.api.get_device_state(self)
        self.json_state = json_state
        #print(json_state)
        return True

    def getVoltage(self):
        return self.json_state.get("charging").get("voltage")

    def getAmps(self):
        return self.json_state.get("charging").get("amps_current")

    def getWatts(self):
        return self.json_state.get("charging").get("watt_power")

    def getStatus(self):
        return self.json_state.get("state")

    def getTemperature(self):
        return self.json_state.get("temperature")

    def getChargeTime(self):
        return self.json_state.get("charging").get("seconds_charging")

    def getEnergyAdded(self):
        return self.json_state.get("charging").get("wh_energy")



#------------------------------------------------------------------------------
#-----------EXECUTION CODE-----------------------------


eMW_histData.run
