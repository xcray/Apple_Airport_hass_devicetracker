#!/usr/bin/python3
from requests import post

import os

host = os.getenv('HA_HOST', '127.0.0.1')
port = os.getenv('HA_PORT', '8123')
token = os.getenv('HA_TOKEN', 'NO TOKEN')

endpoint = 'http://' + host + ':' + port
headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}

while True:
    try:
        str = input()
    except EOFError:
        break
    if 'pppoe: Disconnected.' in str or 'ether: (WAN) link state is Down' in str:
        postData = '{"state":"off","attributes": {"wan_ip":""}}'
        post(endpoint + '/api/states/binary_sensor.Internet',data=postData,headers=headers)
    elif 'pppoe: Connection established' in str:
        wan_ip = str[str.find('established')+12:str.find('->')-1]
        postData = '{"state":"on","attributes": {"wan_ip":"'+wan_ip+'"}}'
        post(endpoint + '/api/states/binary_sensor.Internet',data=postData,headers=headers)
    elif 'Disassociated with station' in str:
        mac = str[-17:len(str)]
        postData = '{"mac":"'+mac+'","source_type":"router","consider_home":"3"}'
        post(endpoint + '/api/services/device_tracker/see',data=postData,headers=headers)
    elif 'Installed unicast CCMP key for supplicant' in str:
        mac = str[-17:len(str)]
        postData = '{"mac":"'+mac+'","source_type":"router","consider_home":"99:00:00"}'
        post(endpoint + '/api/services/device_tracker/see',data=postData,headers=headers)
