import helics as h

print("hello")

print("about to read file")
fed = h.helicsCreateMessageFederateFromConfig("config2.json")
print("read file")
epid = h.helicsFederateGetEndpointByIndex(fed, 0)
ep_name = h.helicsEndpointGetName(epid)
print(ep_name)

h.helicsFederateEnterExecutingMode(fed)
print("Entered Execution mode")
value = 0.0
prevtime = 0
currenttime = -1
while currenttime <= h.helics_time_maxtime:
	print("came in with time", currenttime)
	currenttime = h.helicsFederateRequestTime(fed, h.helics_time_maxtime)
#	print("Granted time", currenttime)
	if(h.helicsEndpointHasMessage(epid)):
		value = h.helicsEndpointGetMessage(epid)
		print("Received value = {} at time {} from PI SENDER".format(value.data, value.time))

h.helicsFederateFinalize(fed)
h.helicsFederateFree(fed)
h.helicsCloseLibrary()
print("PI RECEIVER: Federate finalized")
