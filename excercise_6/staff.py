import time
import helics as h
import random
import logging as log
import subprocess
import os

maxtime = 1e+8

def init_manager(config_file_name, worker_name_list):
	print("manager in")
	fed = h.helicsCreateMessageFederateFromConfig(config_file_name)
	print("manager passed config")
	my_epid = h.helicsFederateGetEndpoint(fed, "data")
	log_id = h.helicsFederateGetEndpoint(fed, "logger")
	log_dest = h.helicsEndpointGetDefaultDestination(log_id)
	
	currenttime = -1
	print("Manager about to Started")
	h.helicsFederateEnterExecutingMode(fed)
	print("Manager Started")
	for t in range(1, 11):
		h.helicsEndpointSendMessageRaw(log_id, log_dest, "Timestep {}".format(t))

		message = "Hello World " + str(t)	
		while currenttime < t:
			currenttime = h.helicsFederateRequestTime(fed, t)

		log_msg = ""

		################### START TIMING ###############
		start_time = time.time_ns() / (10 ** 9)
		##############################################

		for worker_name in worker_name_list:
			h.helicsEndpointSendMessageRaw(my_epid, worker_name + "/data", message)

		while not (h.helicsEndpointPendingMessages(my_epid) == len(worker_name_list)):
			currenttime = h.helicsFederateRequestTime(fed, 0)

		for i in range(len(worker_name_list)):
			if h.helicsEndpointHasMessage(my_epid):
				new_message = h.helicsEndpointGetMessage(my_epid)
				log_msg = log_msg + "From: {}  Msg: {}  Time: {}\n".format(new_message.source, new_message.data, new_message.time)
	
		################### END TIMING ##################
		end_time = time.time_ns() / (10 ** 9)
		###############################################
		
		time_taken = "Time taken for iteration " + str(t) + ": " + str(end_time - start_time) + "\n"
		
		h.helicsEndpointSendMessageRaw(log_id, log_dest, log_msg)	
		h.helicsEndpointSendMessageRaw(log_id, log_dest, time_taken)

	fed_name = h.helicsFederateGetName(fed)
	h.helicsFederateFinalize(fed)
#	print("{}: Federate finalized".format(fed_name))
	h.helicsFederateFree(fed)
	h.helicsCloseLibrary()




def init_worker(config_file_name, manager_name, individual_simulation_time):
	print("worker in")
	fed = h.helicsCreateMessageFederateFromConfig(config_file_name)
	print("worker passed config")
	my_epid = h.helicsFederateGetEndpoint(fed, "data")
	fed_name = h.helicsFederateGetName(fed)
	
	dest = manager_name + "/data"
	pid = os.getpid()
	print(fed_name, " about to Started")
	h.helicsFederateEnterExecutingMode(fed)

	print(fed_name , " Started")
	current_time = -1
	while current_time < maxtime:
		current_time = h.helicsFederateRequestTime(fed, maxtime)
		if h.helicsEndpointHasMessage(my_epid):
			message = h.helicsEndpointGetMessage(my_epid)
			data = str(fed_name) + "(" + str(pid) + "): "  + str(message.data)
#			time.sleep(random.randrange(4))
			time.sleep(individual_simulation_time)
			h.helicsEndpointSendMessageRaw(my_epid, str(dest), data) 

	h.helicsFederateFinalize(fed)
	h.helicsFederateFree(fed)
	h.helicsCloseLibrary()





def init_logger(config_file_name, log_out_file_name, total_simulation_time, individual_simulation_time):
	print("logger in")
	fed = h.helicsCreateMessageFederateFromConfig(config_file_name)
	print("logger passed config")
	my_epid = h.helicsFederateGetEndpoint(fed, "logger")

	fed_name = h.helicsFederateGetName(fed)
#	print(fed_name)
	pid = os.getpid()
#	print("Logger Pid {}".format(pid))
	currenttime = -1
	
	output = ""	
	log.basicConfig(filename="./log/{}".format(log_out_file_name), filemode='w', format='%(message)s', level=log.INFO)

	print(fed_name , " about to Started")
	h.helicsFederateEnterExecutingMode(fed)
	
	print(fed_name , "Started")
	while(currenttime < maxtime):
		currenttime = h.helicsFederateRequestTime(fed, maxtime)
		if h.helicsEndpointHasMessage(my_epid):
			count = h.helicsEndpointPendingMessages(my_epid) 
			for i in range(count):
				message = h.helicsEndpointGetMessage(my_epid)
#				log.log(str(message.messageID))
				output = output + str(message.data) + "message id: " + "\n"
	log.info(output)
	h.helicsFederateFinalize(fed)
	print(fed_name, " : Federate finalized")
	h.helicsFederateFree(fed)
	h.helicsCloseLibrary()



def init_broker(num_federates, comm_type, root):
	if root == "True":
		print("Starting Root")
		command = "helics_broker -f {} --root --type={}".format(num_federates, comm_type)
	elif root == "False":
		print("strating sub brokers")
		command = "helics_broker -f {} --broker_address=0:0 --type={}".format(num_federates, comm_type)
	subprocess.call(command, shell=True)

