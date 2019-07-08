import helics as h


print("about to read file")
fed = h.helicsCreateMessageFederateFromConfig("config2.json")
print("read file")
epid = h.helicsFederateGetEndpointByIndex(fed, 0)
ep_name = h.helicsEndpointGetName(epid)
print(ep_name)

h.helicsFederateEnterExecutingMode(fed)
value = 0.0
prevtime = 0
currenttime = -1
while currenttime <= 100:
	currenttime = h.helicsFederateRequestTime(fed, 1000)
#	print("Granted time", currenttime)
	if(h.helicsEndpointHasMessage(epid)):
		value = h.helicsEndpointGetMessage(epid)
		print("Received value = {} at time {} from PI SENDER".format(value.data, value.time))

h.helicsFederateFinalize(fed)
h.helicsFederateFree(fed)
h.helicsCloseLibrary()
print("PI RECEIVER: Federate finalized")
