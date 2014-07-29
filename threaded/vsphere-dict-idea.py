import calendar
import time
import string
from pysphere import VIServer, VIProperty
import random
from socket import socket
#from threading import Thread
import threading
#Begin Properties
server = VIServer()
HOST = "HostnameOrIPAddress"
USER = "username"
PASSWORD = "password"

CARBON_SERVER = "127.0.0.1"
CARBON_PORT = 2003

delay = 60
interval = 7
prefix = "vsphere2."

sock = socket()

maxPThreads = 3
pThreadDelay = 16


try:
        sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
        print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
        sys.exit(1)
try:
        server.connect(HOST, USER, PASSWORD)
except:
        print "Unable to connect to vsphere server"
        sys.exit(1)
# If this still works than proceed.

pm = server.get_performance_manager()


metricStores = {}

def getVSphereStats():
	global sock, server, pm, metricStores, prefix

#Begin Threads
#	while True:
	if True:
		beganTime = int(time.time())
		for dc_mor, dc_name in server.get_datacenters().items():
			hosts = server.get_hosts(dc_mor)
			for hs_mor, hs_name in hosts.items():
				print "Grabbing Stats for " + dc_name + " - " + hs_name
				gphHSName = hs_name
				gphHSName = gphHSName.replace('.', '_')
				gphHSName = gphHSName.replace(' ', '_')

				counters = pm.get_entity_counters(hs_mor)
				stats = None
				try:
					stats = pm.get_entity_statistic(hs_mor,counters.values())
				except:
					print "I am unable to get performance stat entity for host " + hs_name
				if not stats:
					print "No performance stats could be obtained"
				else:
					for stat in stats:
						instance = stat.instance
						description = stat.description
						group_description = stat.group_description
						unit_description = stat.unit_description
						unit = stat.unit
						counter = stat.counter
						value = stat.value
						group = stat.group
						metric = prefix + dc_name + ".hosts." + gphHSName + "." + group + "."
						if instance <> "":
							instance = instance.replace('.', '_')
							instance = instance.replace('/', '_')
							metric = metric + instance + "."
						metric = metric + counter + "_" + unit_description

						metricStores[metric] = value	
#end function for now
def sendToGraphiteInstance():
	global sock, metricStores,interval
	while True:
		message = ""
		for value, key in enumerate(metricStores):
			now = int(time.time())
			#print key + " " +str(value) + " "
			ln = key + " " + str(value) + " " + str(now)
			#message = message + '\n' + ln + '\n' 
			#message.join('\n' + ln)
			message = message + ln + '\n'
		#print key
		#print value
		#print "--------"

		#print message
		if message:
			sock.sendall(message)
			print "Sent to graphite server"
			print message
			print "Sleeping socket sender for " + str(interval) + " seconds"
			print "........."
		time.sleep(interval)	
#1st cycle to generate the stats and next create the thread daemon to send the hashtable to the server.
getVSphereStats()
#sendToGraphiteInstance()
s = threading.Thread(name='socketThread', target=sendToGraphiteInstance)
s.setDaemon(True)
s.start()
while True:
	getVSphereStats()
	time.sleep(delay)

#print metricStores


