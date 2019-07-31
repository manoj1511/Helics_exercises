import helics as h
import time

initstring = "-f 2 --name=mainbroker"

broker = h.helicsCreateBroker("zmq", "", initstring)

isconnected = h.helicsBrokerIsConnected(broker)

if isconnected == 1:
    print("Broker created and connected")



fed = h.helicsCreateCombinationFederateFromConfig("sender.json")

my_epid = h.helicsFederateGetEndpoint(fed, "data")


h.helicsFederateEnterExecutingMode(fed)

current_time = 0

for i in range(1,11):
	while(current_time < i+1):
		current_time = h.helicsFederateRequestTime(fed, i)
		print("current time : ", current_time)
		if(current_time == i + 0.2):
			h.helicsEndpointSendMessageRaw(my_epid, "receiver/data", str(0.5))
		time.sleep(0.5)
		
		if(h.helicsEndpointHasMessage(my_epid)):
			message = h.helicsEndpointGetMessage(my_epid)
			print("Received message back", message.data, "at time", message.time)

h.helicsFederateFinalize(fed)

while h.helicsBrokerIsConnected(broker):
    time.sleep(1)

h.helicsFederateFree(fed)
h.helicsCloseLibrary()
