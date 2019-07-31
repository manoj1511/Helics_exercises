import staff
import os
import subprocess
import sys
import collections

def unique_ordered_list(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

class Structure:												# A data structure
	def __init__(self, manager_name, worker_name_list, log_config_file_name, total_simulation_time):
		self.manager_name = manager_name
		self.worker_name_list = worker_name_list
		self.log_config_file_name = log_config_file_name
		self.log_out_file_name = log_config_file_name.split(".")[0] + ".log"
		self.worker_list_string = ""
		for worker in self.worker_name_list:
			self.worker_list_string = self.worker_list_string + worker + " "			# This string will be used to pass the list as agrument
		self.total_simulation_time =  total_simulation_time
		self.individual_simulation_time = total_simulation_time / len(worker_name_list)

broker_name = "autobroker"											# Name of the broker
comm_type = "mpi"												# name of the core used


manager_name = "manager_1"
worker_name_list = ["worker_A", "worker_B", "worker_C"]
log_config_file_name = "logger_1.json"
total_simulation_time = 0.10											# Simulation time that we are trying to reduce using parallelization

## Initialize the data structure
data_1 = Structure(manager_name, worker_name_list, log_config_file_name, total_simulation_time)						

manager_name = "manager_2"
worker_name_list = ["worker_D", "worker_E", "worker_F"]
log_config_file_name = "logger_2.json"

## Initialize the data structure
data_2 = Structure(manager_name, worker_name_list, log_config_file_name, total_simulation_time)						



## configure the nodes
nodefile = os.environ["PBS_NODEFILE"]										# Requested node configuration using slurm is available in this file $PBS_NODEFILE
file_handle = open(nodefile,"r")										# Open the file
file_handle = file_handle.readlines()										# Read all the lines to a list. Contains extra server name alon with node name eg. abc.server.com
node_names = []													# A list to store the node names
for node in file_handle:											# Loop through the lines
	node_names.append(node.split(".")[0])									# split at "." and append only the first element that containes node name to node_names list

unique_nodes = unique_ordered_list(node_names)
print(unique_nodes)



## configurations
num_broker_1_federates = len(data_1.worker_name_list) + 1 + 1							# num_worker + num_managers + num_loggers
num_broker_2_federates = len(data_2.worker_name_list) + 1 + 1

total_federates = num_broker_1_federates + num_broker_2_federates 					

if(node_names.count(unique_nodes[0]) < 1 or node_names.count(unique_nodes[1]) < num_broker_1_federates + 1 or node_names.count(unique_nodes[2]) < num_broker_2_federates + 1):			
	print("requested wrong configuration")
	print("request a chunck for root broker with atleast 1 mpi process, request other chuncks with atleast 1 mpiprocess for broker, 1 mpiprocess for logger, 1 mpiprocess for manager and num_workers mpiprocess for workers")
	sys.exit()


init_string = ""												# String that will be written to MPI config file				

## Brokers Initialization
init_string = init_string + "-np 1 --host {} python broker.py {} {} {}".format(unique_nodes[0], total_federates, comm_type, True) + "\n" 
init_string = init_string + "-np 1 --host {} python broker.py {} {} {}".format(unique_nodes[1], num_broker_1_federates, comm_type, False) + "\n" 
init_string = init_string + "-np 1 --host {} python broker.py {} {} {}".format(unique_nodes[2], num_broker_2_federates, comm_type, False) + "\n" 

## Federation 1 Initialization
init_string = init_string + "-np 1 --host {} python manager.py {} {}".format(unique_nodes[1], "./configuration/" + data_1.manager_name + ".json" , data_1.worker_list_string) + "\n"
for file_name in data_1.worker_name_list:
	init_string = init_string + "-np 1 --host {} python worker.py {} {} {}".format(unique_nodes[1], "./configuration/" + file_name + ".json", data_1.manager_name, data_1.individual_simulation_time) + "\n"
init_string = init_string + "-np 1 --host {} python logger.py {} {} {} {}".format(unique_nodes[1], "./configuration/" + data_1.log_config_file_name, data_1.log_out_file_name, data_1.total_simulation_time, data_1.individual_simulation_time) + "\n"

## Federation 2 Initialization
init_string = init_string + "-np 1 --host {} python manager.py {} {}".format(unique_nodes[2], "./configuration/" + data_2.manager_name + ".json" , data_2.worker_list_string) + "\n"
for file_name in data_2.worker_name_list:
	init_string = init_string + "-np 1 --host {} python worker.py {} {} {}".format(unique_nodes[2], "./configuration/" + file_name + ".json", data_2.manager_name, data_2.individual_simulation_time) + "\n"
init_string = init_string + "-np 1 --host {} python logger.py {} {} {} {}".format(unique_nodes[2], "./configuration/" + data_2.log_config_file_name, data_2.log_out_file_name, data_1.total_simulation_time, data_1.individual_simulation_time) + "\n"


# Write the mpi config file
file = open("init-mpi.conf", "w")										# Write the Mpi config file which will be read by mpirun
file.write(init_string)
file.close()

mpi_runner = subprocess.call("mpirun --app init-mpi.conf", shell = True)					# Run the mpirun with the configuration file using a subprocess call 
print("Exit status: {}".format(mpi_runner))									# Returns after MPI finishes its job

