import calendar
import time
import string
from socket import socket
from pysphere import VIServer, VIProperty

server = VIServer()

CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
delay = 15

HOST = "HostnameOrIPAddress"
USER = "username"
PASSWORD = "password"
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
pm = server.get_performance_manager()

while True:
	lines = []
	for dc_mor, dc_name in server.get_datacenters().items():
		now = int(time.time())
		datastores = server.get_datastores(dc_mor)
		for ds_mor, ds_name in datastores.items():
			gphDSName = ds_name.replace('.', '_')
			gphDSName = gphDSName.replace(' ', '_')
			props = VIProperty(server, ds_mor)
			lines.append(prefix + dc_name + ".datastores." + props.summary.type + "." + gphDSName + ".capacity " + str(props.summary.capacity) + " " + str(now))
                	lines.append(prefix + dc_name + ".datastores." + props.summary.type + "." + gphDSName + ".freespace " + str(props.summary.freeSpace) + " " +str(now))
			if hasattr(props.summary, "uncommitted"):
				lines.append(prefix + dc_name + ".datastores." + props.summary.type + "." + gphDSName + ".uncommitted " + str(props.summary.uncommitted) + " " + str(now))
	message = '\n'.join(lines) + '\n'
	sock.sendall(message)
	print message
	time.sleep(delay)
server.disconnect()
