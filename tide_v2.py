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
from termcolor import cprint

station = 9413745  # santa cruz, ca
api_key = "dW75tItAEyByLNGyE7lSLl" # IFTTT webhook api key


# build url and cal api to get json data
def call_url():
    d = datetime.datetime.now()
    fD = d + datetime.timedelta(days=7)
    nD = d.strftime("%Y%m%d")
    fD = fD.strftime("%Y%m%d")
    url = "https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=\
     NOS.COOPS.TAC.WL&begin_date=" + nD + "&end_date=" + fD + "&datum=MLLW&station="\
     + str(station) + "&time_zone=lst_ldt&units=english&interval=hilo&format=json"
    r = requests.get(url)
    data = r.json()
    return data


# look through json data to find tides less than negative 1 then call alert
def seaglass(data):
    for x in data['predictions']:
        if float(x['v']) <= -1:
            if datetime.datetime.strptime(x['t'], '%Y-%m-%d %H:%M').weekday()in {5, 6}:
                if 20 > datetime.datetime.strptime(x['t'], '%Y-%m-%d %H:%M').hour >= 6:
                    t = str(x['v'] + " " + x['t'])
                    alert(t)
            elif 20 > datetime.datetime.strptime(x['t'], '%Y-%m-%d %H:%M').hour > 16:
                t = str(x['v'] + " " + x['t'])
                alert(t)


# send webhook to IFTTT with data
def alert(date_tide):
    url = 'https://maker.ifttt.com/trigger/tide/with/key/' + api_key
    payload = {}
    payload["value1"] = date_tide
    r = requests.post(url, data=payload)


data = call_url()
seaglass(data)
alert('test')
