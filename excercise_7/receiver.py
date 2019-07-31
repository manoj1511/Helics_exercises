import helics as h
import time

maxtime = 1e5

fed = h.helicsCreateCombinationFederateFromConfig("receiver.json")


my_epid = h.helicsFederateGetEndpoint(fed, "data")

h.helicsFederateEnterExecutingMode(fed)

current_time = -1

while current_time < maxtime:
	current_time = h.helicsFederateRequestTime(fed, maxtime)
	if(h.helicsEndpointHasMessage(my_epid)):
		message = h.helicsEndpointGetMessage(my_epid)
		print("got the message", message.data, "so i'm going to sleep", message.data, "s at time", message.time)
		h.helicsFederateRequestTimeAsync(fed, current_time + float(message.data))
		time.sleep(5)	
		current_time = h.helicsFederateRequestTimeComplete(fed)
		h.helicsEndpointSendMessageRaw(my_epid, "sender/data", "Completed")	


h.helicsFederateFinalize(fed)

h.helicsFederateFree(fed)
h.helicsCloseLibrary()


