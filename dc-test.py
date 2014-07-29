import string
import calendar
import time
from pysphere import VIServer, VIProperty
from socket import socket

server = VIServer()
HOST = "HostnameOrIPAddress"
USER = "username"
PASSWORD = "password"

CARBON_SERVER = "127.0.0.1"
CARBON_PORT = 2003

prefix = "vsphere."


server.connect(HOST, USER, PASSWORD)
pm = server.get_performance_manager()
lines = []
for dc_mor, dc_name in server.get_datacenters().items():
	#print dc_name
	now = int( time.time() )
	datastores = server.get_datastores(dc_mor)
	for ds_mor, ds_name in datastores.items():
		gphDSName = ds_name.replace('.','_')
		gphDSName = gphDSName.replace(' ', '_')
		#print prefix + dc_name + ".datastores." + gphDSName
		props = VIProperty(server, ds_mor)
		lines.append(prefix + dc_name + ".datastores." + props.summary.type + "." + gphDSName + ".capacity " + str(props.summary.capacity) + str(now))	
	#	print prefix + dc_name + ".datastores." + props.summary.type + "." + gphDSName + ".capacity " + str(props.summary.capacity) + str(now)
		lines.append(prefix + dc_name + ".datastores." + props.summary.type + "." + gphDSName + ".freespace " + str(props.summary.freeSpace) + str(now))
	#	print prefix + dc_name + ".datastores." + props.summary.type + "." + gphDSName + ".freespace " + str(props.summary.freeSpace) + str(now)
		if hasattr(props.summary, "uncommitted"):
			lines.append(prefix + dc_name + ".datastores." + props.summary.type + "." + gphDSName + ".uncommitted " + str(props.summary.uncommitted) + str(now))		

	hosts = server.get_hosts(dc_mor)
	for hs_mor, hs_name in hosts.items():
		gphHostName = hs_name.replace('.','_')
#		print dc_name + "." +hs_name
		#print prefix + dc_name + ".hosts." + gphHostName
		props = VIProperty(server, hs_mor)
		print props
		counters = pm.get_entity_counters(hs_mor)
		
		for counter_name, counter_val in counters.items():
			stats = pm.get_entity_statistic(hs_mor, counter_val)
			if not stats: 
				print "Nothing"
			for stat in stats:
				lines.append(prefix + dc_name + ".hosts." + gphHostName + "." + stat.unit_description + "." + stat.counter + " " + str(stat.value) + " " + str(now))
		
#	print dc_mor
	#We need to get datastores and host statistics
#	for hs_mor, hs_name in dc_mor.get_hosts().items():
#		print hs_name
#for hs_mor, hs_name in server.get_hosts().items():
#	print hs_mor.get_properties()
message = '\n'.join(lines) +'\n'
print message
server.disconnect()	
