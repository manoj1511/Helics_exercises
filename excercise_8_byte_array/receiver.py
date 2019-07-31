import helics as h
import time
import struct

maxtime = 1e5

fed = h.helicsCreateCombinationFederateFromConfig("receiver.json")


my_epid = h.helicsFederateGetEndpoint(fed, "data")

h.helicsFederateEnterExecutingMode(fed)

current_time = -1

while current_time < maxtime:
	current_time = h.helicsFederateRequestTime(fed, maxtime)
	if(h.helicsEndpointHasMessage(my_epid)):
		message = h.helicsEndpointGetMessage(my_epid)
		print(type(message.data))
		print(message.data)
		print(list(message.data))	
h.helicsFederateFinalize(fed)
h.helicsFederateFree(fed)
h.helicsCloseLibrary()

