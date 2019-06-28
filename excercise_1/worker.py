from federate import Federate
import helics as h
import random
import time

helicsversion = h.helicsGetVersion()
print("Worker: Helics version = {}".format(helicsversion))

fed = []
n = 10

for i in range(n):
	
	fed.append(Federate())
	fed_name = str("worker" + str(i) + "federate")
	fed[i].create_federate(fed_name)
	fed[i].subscribe("manager_time")
	fed[i].subscribe("manager")
	pub_name = str('worker' + str(i))
	fed[i].publish(pub_name, "double")

for i in range(n):
	fed[i].start_async()

for i in range(n):
	h.helicsFederateEnterExecutingModeComplete(fed[i].vfed)	
#	print(i, "started")

for i in range(n):
	currenttime = h.helicsFederateRequestTime(fed[i].vfed, 0)

currenttime = -1

it = 0
while not it == 11:
	for i in range(n):
		if(h.helicsInputIsUpdated(fed[i].sub[0])):
			currenttime = h.helicsInputGetTime(fed[i].sub[0])
			print("Worker", i, ": Received time =", currenttime, "from Manager")
			currenttime = h.helicsFederateRequestTime(fed[i].vfed, currenttime+1)
		else:
			currenttime = h.helicsFederateRequestTime(fed[i].vfed, currenttime+1)
		if h.helicsInputIsUpdated(fed[i].sub[1]):
			value = h.helicsInputGetDouble(fed[i].sub[1])
			print("Worker", i, ": Received value =", value ,"at time =", currenttime,"from Manager")
			value = value * (i+2)
			time.sleep(random.randrange(2))			
			h.helicsPublicationPublishDouble(fed[i].pub[0], value)
			print("Worker", i, ": Sending value =", value, "at time =", currenttime ,"to Manager")
			print("-----------------------------------------------------------")
			if i == n - 1:
				it = it + 1
for i in fed:
	i.destroy()

print("federates finalized")
h.helicsCloseLibrary()
