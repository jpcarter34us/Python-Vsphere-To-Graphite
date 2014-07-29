
from pysphere import VIServer, VIProperty 

server = VIServer() 
HOST = "HostnameOrIPAddress"
USER = "username"
PASSWORD =  "password"

server.connect(HOST, USER, PASSWORD) 

for ds_mor, name in server.get_datastores().items(): 
    props = VIProperty(server, ds_mor) 
    print "DATASTORE:", name 
    print "  Type:", props.summary.type 
    print "  Capacity:", props.summary.capacity 
    print "  Free space:", props.summary.freeSpace 
    if hasattr(props.summary, "uncommitted"): 
        print "  Uncommited:", props.summary.uncommitted 

server.disconnect() 
