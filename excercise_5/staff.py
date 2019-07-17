import time
import helics as h
import random
import logging as log
import subprocess
import os

maxtime = 1e+8

def init_manager(config_file_name, worker_name_list):
	fed = h.helicsCreateMessageFederateFromConfig(config_file_name)

	my_epid = h.helicsFederateGetEndpoint(fed, "data")
	log_id = h.helicsFederateGetEndpoint(fed, "logger")
	log_dest = h.helicsEndpointGetDefaultDestination(log_id)
		
	currenttime = -1
	h.helicsFederateEnterExecutingMode(fed)

	for t in range(1, 11):
		h.helicsEndpointSendMessageRaw(log_id, log_dest, "Timestep {}".format(t))

		message = "Hello World " + str(t)	
		while currenttime < t:
			currenttime = h.helicsFederateRequestTime(fed, t)

		for worker_name in worker_name_list:
			h.helicsEndpointSendMessageRaw(my_epid, worker_name + "/data", message)

		while not (h.helicsEndpointPendingMessages(my_epid) == len(worker_name_list)):
			currenttime = h.helicsFederateRequestTime(fed, 0)
		log_msg = ""
		for i in range(len(worker_name_list)):
			if h.helicsEndpointHasMessage(my_epid):
				new_message = h.helicsEndpointGetMessage(my_epid)
				log_msg = log_msg + "From: {}  Msg: {}  Time: {}\n".format(new_message.source, new_message.data, new_message.time)
	
		h.helicsEndpointSendMessageRaw(log_id, log_dest, log_msg)

	fed_name = h.helicsFederateGetName(fed)
	h.helicsFederateFinalize(fed)
	
#	print("{}: Federate finalized".format(fed_name))

	h.helicsFederateFree(fed)
	h.helicsCloseLibrary()




def init_worker(config_file_name, manager_name):
	fed = h.helicsCreateMessageFederateFromConfig(config_file_name)

	my_epid = h.helicsFederateGetEndpoint(fed, "data")
	fed_name = h.helicsFederateGetName(fed)
	
	dest = manager_name + "/data"
	pid = os.getpid()
	h.helicsFederateEnterExecutingMode(fed)

	current_time = -1
	while current_time < maxtime:
		current_time = h.helicsFederateRequestTime(fed, maxtime)
		if h.helicsEndpointHasMessage(my_epid):
			message = h.helicsEndpointGetMessage(my_epid)
			data = str(fed_name) + "(" + str(pid) + "): "  + str(message.data)
#			time.sleep(random.randrange(4))
			h.helicsEndpointSendMessageRaw(my_epid, str(dest), data) 

	h.helicsFederateFinalize(fed)

	h.helicsFederateFree(fed)
	h.helicsCloseLibrary()





def init_logger(config_file_name):
	fed = h.helicsCreateMessageFederateFromConfig(config_file_name)
	my_epid = h.helicsFederateGetEndpoint(fed, "logger")

	fed_name = h.helicsFederateGetName(fed)
	print(fed_name)
	pid = os.getpid()
	print("Logger Pid {}".format(pid))
	currenttime = -1

	output = ""	

	log.basicConfig(filename='./log/logger.log', filemode='w', format='%(message)s', level=log.INFO)

	h.helicsFederateEnterExecutingMode(fed)
	while(currenttime < maxtime):
		currenttime = h.helicsFederateRequestTime(fed, maxtime)
		if h.helicsEndpointHasMessage(my_epid):
			count = h.helicsEndpointPendingMessages(my_epid) 
			for i in range(count):
				message = h.helicsEndpointGetMessage(my_epid)
				output = output + str(message.data) + "\n"
	log.info("Current Time : {}".format(currenttime))
	log.info(output)
	h.helicsFederateFinalize(fed)
	print(fed_name, " : Federate finalized")
	h.helicsFederateFree(fed)
	h.helicsCloseLibrary()



def init_broker(num_federates, broker_name):
	command = "helics_broker -f{} -n{}".format(num_federates, broker_name)
	subprocess.call(command, shell=True)
