"""stuff."""
import requests
import time
import homeassistant.remote as remote

url = 'http://192.168.1.112'
motion = 'http://192.168.1.112/setSystemMotion'
headers = {
    'Origin': 'http://192.168.1.112',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://192.168.1.112/setSystemMotion',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8'}

api = remote.API('hassio.local', 'blackjack4')
home = ''
last_home = 'start'

while True:
    # try getting state from HA
    try:
        home = remote.get_state(api, 'group.all_devices')
    except Exception as e:
        print(e)
        continue
    if home == last_home:
#        print('.')
        time.sleep(10)
        continue
    if type(home) == 'NoneType':
        time.sleep(10)
        continue

    print(time.strftime('%a %H:%M:%S'), ' - {}: {}'.format(home.name, home.state))

    # set payload based on HA response
    if home.state == 'home':
        onoff = 0
    else:
        onoff = 1

    # setup request to ip cam
    payload = {'MotionDetectionEnable':	onoff, 'ConfigSystemMotion': 'Save'}
    s = requests.Session()
    s.auth = ('admin', 'Sword44Weed')

    # try sending payload to ip cam
    try:
        r = s.get(url)
        r = s.post(motion, data=payload, headers=headers)
#        print('fired')
    except Exception as e:
        print(e)
        continue

    # print status of motion detection
    if payload['MotionDetectionEnable'] == 0:
        onoff = 'off'
    else:
        onoff = 'on'

    print(time.strftime('%a %H:%M:%S'), ' - Motion is {}'.format(onoff))
    last_home = home
    time.sleep(10)
