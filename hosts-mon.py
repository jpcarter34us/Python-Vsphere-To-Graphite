import calendar
import time
import string
from pysphere import VIServer, VIProperty
from socket import socket

server = VIServer()
HOST = "HostnameOrIPAddress"
USER = "username"
PASSWORD = "password"

CARBON_SERVER = "127.0.0.1"
CARBON_PORT = 2003

delay = 60
prefix = "vsphere."

sock = socket()
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

while True:
	#lines = []
	#now = int(time.time())
	beganTime = int(time.time())
	for dc_mor, dc_name in server.get_datacenters().items():
		hosts = server.get_hosts(dc_mor)
		for hs_mor, hs_name in hosts.items():
			#time = int(time.time())
			lines = None
			lines = []
			now = int(time.time())
			print "Grab metric for host " + hs_name + " in Datacenter " + dc_name
			gphHSName = hs_name
			gphHSName = gphHSName.replace('.', '_')
			gphHSName = gphHSName.replace(' ', '_')
			
			counters = pm.get_entity_counters(hs_mor)
			
			stats = None
			stat_continue = True
			try:
				stats = pm.get_entity_statistic(hs_mor, counters.values())
			except: 
				print "I am unable to get performance stat entity for host " + gphHSName
			
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
					
					metric = prefix + dc_name + ".hosts." +gphHSName + "." + group + "."
					if instance <> "":
						#temporarily replace metric / with . to create new keys.
						instance = instance.replace('.', '_')
						instance = instance.replace('/', '.')
						metric = metric + instance + "." 
					metric = metric + counter + "_" + unit_description
					sndMetric = metric + " " + value + " " + str(now)
					lines.append(sndMetric)
					#print sndMetric
			if stats:
				message = None
				message = '\n'.join(lines) + '\n'
				sock.sendall(message)
				print message
				print "--------------------"	
#	message = '\n'.join(lines) + '\n'
#	sock.sendall(message)
#	print message
	endTime = int(time.time())
	iterationTime = endTime - beganTime
	print "It took " + str(iterationTime) + " to grab hosts metrics"
	print "Delay for " + str(delay)
	time.sleep(delay)
server.disconnect()
socket.close()

