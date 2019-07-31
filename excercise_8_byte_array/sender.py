import helics as h
import time
import struct

initstring = "-f 2 --name=mainbroker"

broker = h.helicsCreateBroker("zmq", "", initstring)

isconnected = h.helicsBrokerIsConnected(broker)

if isconnected == 1:
    print("Broker created and connected")



fed = h.helicsCreateCombinationFederateFromConfig("sender.json")
my_epid = h.helicsFederateGetEndpoint(fed, "data")


h.helicsFederateEnterExecutingMode(fed)


l = []
for i in range(64, 79):
	l.append(i)
l.append(255)
message = bytes(l)

print(message)

current_time = 0
for i in range(1, 5):
	current_time = h.helicsFederateRequestTime(fed, i)
	print("current time : ", current_time)
		
	h.helicsEndpointSendMessageRaw(my_epid, "receiver/data", message)
	time.sleep(0.5)
		

h.helicsFederateFinalize(fed)

while h.helicsBrokerIsConnected(broker):
    time.sleep(1)

h.helicsFederateFree(fed)
h.helicsCloseLibrary()
