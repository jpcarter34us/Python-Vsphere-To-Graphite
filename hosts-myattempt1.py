import string
from pysphere import VIServer
server = VIServer()
HOST = "HostnameOrIPAddress"
USER = "username"
PASSWORD = "password"
server.connect(HOST, USER, PASSWORD)
pm = server.get_performance_manager()

prefix = "vsphere.hosts."
for hs_mor, name in server.get_hosts().items():
#	print "Host ", name
	counters = pm.get_entity_counters(hs_mor)
#	for counter in counters:
#		print counter
#		print counter.values()
#	for counter in counters.values():
#		print counter
#	gphHostName = changeHostName(name)
#	gphHostName = name.maketrans('.','_')
	gphHostName = name.replace('.','_')

	for counter_name, counter_val in counters.items():
	#	print counter_name, " ", counter_val
		stats = pm.get_entity_statistic(hs_mor, counter_val)
	#	print stats
		if not stats:
			print "Nothing"
		for stat in stats:
			#print "Counter ",stat.counter
			#print "Value ",stat.value
			print "Description",stat.description
			print "Stat Group: ",stat.group
			print "Group Desc: ",stat.group_description
			#print "Unit name: ", stat.unit
			#print "Unit Desc: ", stat.unit_description
			#print "----------------"
			gpMetric = prefix + gphHostName + "." + stat.unit_description + "." + stat.counter + " " + stat.value + " " + "0"
			print gpMetric
			print "--------------------------"
			#print " ", stat 
	#stats = pm.get_entity_statistic(hs_mor, counters.values())
	#if not stats:
	#	print "No Stat could be found for host ", name
	#for stat in stats:
	#	print " ", stat	

server.disconnect()
def changeHostName(hostNmIn):
	return hostNmIn.maketrans('.','_')
#end function
