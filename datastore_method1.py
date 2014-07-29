from pysphere import VIServer

HOST = "HostnameOrIPAddress"
USER = "username"
PASSWORD = "password"
server = VIServer() 
server.connect(HOST, USER, PASSWORD) 

pm = server.get_performance_manager() 

for ds_mor, name in server.get_datastores().items(): 
    print "ENTITY STATISTICS FOR DATASTORE", name 
    counters = pm.get_entity_counters(ds_mor) 
    print "  Available counters:", ",".join(counters.keys()) 
    stats = pm.get_entity_statistic(ds_mor, counters.values()) 
    if not stats: 
        "  No perf values could be obtained." 
    for stat in stats: 
        print " *", stat 

server.disconnect() 
