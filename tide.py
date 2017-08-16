# -----------------------------------------------------------------------------------------------
#
# Download tide table and print high and low plus times
#
# Python 2.7
#
# Author:
#
#    _____  .__                    _________                    __    __
#   /  _  \ |  |   ____ ___  ___  /   _____/____ ___  _______ _/  |__/  |_  ____   ____   ____
#  /  /_\  \|  | _/ __ \\  \/  /  \_____  \\__  \\  \/ /\__  \\   __\   __\/  _ \ /    \_/ __ \
# /    |    \  |_\  ___/ >    <   /        \/ __ \\   /  / __ \|  |  |  | (  <_> )   |  \  ___/
# \____|__  /____/\___  >__/\_ \ /_______  (____  /\_/  (____  /__|  |__|  \____/|___|  /\___  >
#         \/          \/      \/         \/     \/           \/                       \/     \/
#
# -----------------------------------------------------------------------------------------------

# Import Libraries
import requests
import datetime


station = 9413745  # santa cruz, ca
weekend_hrs = 6 # only send alert for
api_key = 'dW75tItAEyByLNGyE7lSLl'

def seaglass(data):
    for x in data['predictions']:
        if float(x['v']) < -1:
            if datetime.datetime.strptime(x['t'], '%Y-%m-%d %H:%M').weekday()in {5, 6}:
                if 20 > datetime.datetime.strptime(x['t'], '%Y-%m-%d %H:%M').hour >= 6:
                    t = str(x['v'] + " " + x['t'])
                    date_tide(t)
                    t = str(x['t'] + " local time " + x['v'])
                    print t
                elif 20 > datetime.datetime.strptime(x['t'], '%Y-%m-%d %H:%M').hour > 16:
                    t = str(x['t'] + " local time " + x['v'])
                    print t


def printTide(data):
    for x in data['predictions']:
        print x['t'] + " local time", x['type'], x['v']


def alert(date_tide):
    url = 'https://maker.ifttt.com/trigger/tide/with/key/' + api_key
    payload = {}
    payload["value1"] = date_tide
    r = requests.post(url, data=payload)


# Input - load a tide table
# build url
d = datetime.datetime.now()
fD = d + datetime.timedelta(days=7)
nD = d.strftime("%Y%m%d")
fD = fD.strftime("%Y%m%d")

url = "https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=\
 NOS.COOPS.TAC.WL&begin_date=" + nD + "&end_date=" + fD + "&datum=MLLW&station="\
 + str(station) + "&time_zone=lst_ldt&units=english&interval=hilo&format=json"

# Call NOAA API
r = requests.get(url)
data = r.json()

# Look through table for negative tides
# Print out hi-lo and times for todays (send an alert via IFTTT)
print '\n'
print("Seaglass")
seaglass(data)
print '\n'
print("Next 5 Days")
printTide(data)
print '\n'
