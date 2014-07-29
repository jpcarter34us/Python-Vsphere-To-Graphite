import calendar
import time
import string
from pysphere import VIServer, VIProperty
from socket import socket
from threading import Thread
import random

#Begin Class
class performanceThread(Thread):
        sock = None
        server = None
	dc_name = None
        hs_mor = None
        hs_name = None
        pm = None
	prefix = None
        def __init__(self):
                Thread.__init__(self)

        def printVariable(self):
                print self.hs_name
		print self.dc_name
		print server
		#time.sleep(1)
	def run(self):
		beginTTime = int(time.time())
		rndVal = 5
		rndVal = random.randint(1,25)
		print "Thread waiting for " + str(rndVal) + " to initiate."
		time.sleep(rndVal)
		print "Ready " + self.hs_name
		self.printVariable()
		self.runMetricGrab()
		endTTime = int(time.time())
		iitTime = endTTime - beginTTime
		print "Thread completed execution in " + str(iitTime) + " seconds."
		print "Done -----"
	def runMetricGrab(self):
		lines = None
		lines = []
		now = int(time.time())
		gphHSName = self.hs_name
		gphHSName = gphHSName.replace('.', '_')
		gphHSName = gphHSName.replace(' ', '_')
		
		counters = pm.get_entity_counters(self.hs_mor)
		
		stats = None
		stat_continue = True
		try:
			stats = self.pm.get_entity_statistic(self.hs_mor, counters.values())
		except:
			print "I am unable to get performance statistics entity for host " + gphHSName
		#end try.
		
		if not stats:
			print "No performance stats could be obtained"
		else:
			for stat in stats:
#				print stat

				instance = stat.instance
                                description = stat.description
                                group_description = stat.group_description
                                unit_description = stat.unit_description
                               	unit = stat.unit
                               	counter = stat.counter
                                value = stat.value
                                group = stat.group
				#print group
				#print gphHSName
				#print self.prefix
				metric = self.prefix + self.dc_name + ".hosts." + gphHSName + "." + group + "."
				if instance <> "":
					instance = instance.replace('.', '_')
					instance = instance.replace('/', '.')
					metric = metric + instance + "."
				metric = metric + counter + "_" + unit_description
				sndMetric = metric + " " + value + " " + str(now)
				lines.append(sndMetric)
		if stats:
			message = None
			message = '\n'.join(lines) + '\n'
			self.sock.sendall(message)
			print message
			print "-------------------------"

		
#End Class

#Begin Properties
server = VIServer()
HOST = "HostnameOrIPAddress"
USER = "username"
PASSWORD = "password"

CARBON_SERVER = "127.0.0.1"
CARBON_PORT = 2003

delay = 60
prefix = "vsphere."

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
threads = []
#while True:
if True:
	beganTime = int(time.time())
	pThreadCtr = 0
	for dc_mor, dc_name in server.get_datacenters().items():
		hosts = server.get_hosts(dc_mor)
		for hs_mor, hs_name in hosts.items():
			print "begin thread for " + hs_name
			pb = performanceThread()
			pb.sock = sock
			pb.server = server
			pb.hs_mor = hs_mor
			pb.hs_name = hs_name
			pb.pm = pm
			pb.dc_name = dc_name
			pb.prefix = prefix
			#The rest of the stat processes will be in the thread.
			#pb.setDaemon(True)
			#pb.printVariable()
			pb.start()
			threads += [pb]
			#pb.printVariable()
			#pb.runMetricGrab()
			print "end thread for " + hs_name
			pThreadCtr = pThreadCtr + 1
			if pThreadCtr == maxPThreads:
				pThreadCtr = 0
				#print "Hit maximum Threads sleeping for " + str(pThreadDelay) + " seconds."
				#time.sleep(pThreadDelay)
	#define ending variables
#	for x in threads:
#		x.join()
	endTime = int(time.time())
	iterationTime = endTime - beganTime
	print "It took " + str(iterationTime) + " to grab hosts metrics"
	print "Delay for " + str(delay)
#	time.sleep(delay)
#server.disconnect()
#sock.close()
