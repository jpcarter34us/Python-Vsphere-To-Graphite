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
	sock.connect( (CARBON_SERVER, CARBON_PORT) )
except:
	print "Couldn't connect to %(server)s on port %(port)d, is the carbon agent runing?" % {'server':CARBON_SERVER, 'port':CARBON_PORT}
	sys.exit(1)
try:
	server.connect(HOST, USER, PASSWORD)
except:
	print "Unable to connect to vsphere server"
	sys.exit(1)

pm = server.get_performance_manager()
while True:
	timeBegan = int(time.time())
	for dc_mor, dc_name in server.get_datacenters().items():
		datastores = server.get_datastores(dc_mor)
		for ds_mor, ds_name in datastores.items():
			lines = None
			lines = []
			now = int(time.time())
			

			gphDSName = ds_name
			gphDSName = gphDSName.replace(' ', '_')
			gphDSName = gphDSName.replace('.', '_')
			counters = None
			counters = pm.get_entity_counters(ds_mor)
				
			stats = None
			try:
				stats = pm.get_entity_statistic(ds_mor, counters.values())
			except:
				print "I am unable to get performance stat entity for datastore " + gphDSName
				
			if not stats: 
				print "No performance stats could be obtained"
			else:
				props = None
				props = VIProperty(server, ds_mor)
				for stat in stats:
					instance = stat.instance
					description = stat.description
					group_description = stat.group_description
					
					unit_description = stat.unit_description
					unit = stat.unit
					counter = stat.counter
					value = stat.value
					group = stat.group
					pType = props.summary.type

					metric = prefix + dc_name + ".datastores."+ pType + "." + gphDSName + "." + group + "."
					if instance <> "":
						instance = instance.replace('.', '_')
						instance = instance.replace(' ', '_')
						metric = metric + instance + "."
					metric = metric + counter + "_" + unit_description
					sndMetric = metric + " " + value + " " + str(now)
					lines.append(sndMetric)
					#print sndMetric
				if stats:
					message = None
					message = '\n' . join(lines) + '\n'
					sock.sendall(message)
					print message
					print "----------------------------"
	timeDone = int(time.time())
	timeDuration = timeDone - timeBegan
	print "It took " + str(timeDuration) + " to generate and populate the statistics."
	print "Delay for " + str(delay)
	time.sleep(delay)
server.disconnect()
socket.close()
