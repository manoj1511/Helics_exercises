import time
import helics as h
from math import pi

print("about to read file")
fed = h.helicsCreateMessageFederateFromConfig("config1.json")
print("read file")

epid = h.helicsFederateGetEndpointByIndex(fed, 0)
ep_name = h.helicsEndpointGetName(epid)
print(ep_name)

h.helicsFederateEnterExecutingMode(fed)

this_time = 0.0
value = pi

for t in range(1, 11):
    val = value * t
    currenttime = h.helicsFederateRequestTime(fed, t)
    h.helicsEndpointSendMessageRaw(epid, "end2", str(val))
    print("PI SENDER: Sending value pi = {} at time {} to PI RECEIVER".format(val, currenttime))
    time.sleep(1)

h.helicsFederateFinalize(fed)
print("PI SENDER: Federate finalized")

h.helicsFederateFree(fed)
h.helicsCloseLibrary()

