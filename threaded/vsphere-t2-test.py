import random
import calendar
import time
import threading
from pysphere import VIServer, VIProperty
from socket import socket

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



server.disconnect()
sock.close()
