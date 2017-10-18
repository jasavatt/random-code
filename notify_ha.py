#! /usr/bin/env python

import os, time
import paho.mqtt.publish as publish

path = '/home/pi/IP_vids/'
lastT = time.ctime(max(os.stat(root).st_mtime for root,_,_ in os.walk(path)))

print(time.strftime('%a %H:%M:%S'), " - Start")

def alert(state):
	publish.single("cam/alert", payload=state,
	retain=True, hostname="192.168.1.185",
	port=1883, client_id="camAlert",
	auth = {'username':"esp", 'password':"blackjack4"})


while True:
	folderT = time.ctime(max(os.stat(root).st_mtime for root,_,_ in os.walk(path)))
	
	if folderT != lastT:
		# fire api rest
		try: alert("ON")
		except Exception as e: print(e) 
		print(time.strftime('%a %H:%M:%S'),' - triggered!')
		time.sleep(10)
		try: alert("OFF")
		except Exception as e: print(e)
		lastT = time.ctime(max(os.stat(root).st_mtime for root,_,_ in os.walk(path)))
	else:
		time.sleep(10)
