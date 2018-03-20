###############################################################################
#
# Trigger webhook on IFTTT
#
# Author: Alex Savattone
#
# Python 3.X
#
# Change Log:
# 3-19-18 initial
#
###############################################################################

import requests
from sys import argv

api_key = 'epBsMRdmppeL3QohvEhJL'
event = 'alert'
url = 'https://maker.ifttt.com/trigger/{}/with/key/{}'

def hook(v1, v2='', v3=''):
    if type(v1) is 'list':
        v1 = v1[0]
    payload = {'value1': v1, 'value2': v2, 'value3': v3}
    r = requests.post (url.format(event, api_key), json=payload)
    pass

if __name__ == '__main__':
    hook(argv[1:])