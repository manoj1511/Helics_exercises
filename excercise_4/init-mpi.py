import staff
import os
import subprocess
import sys

class Structure:												# A data structure
	def __init__(self, manager_name, worker_name_list, log_config_file_name):
		self.manager_name = manager_name
		self.worker_name_list = worker_name_list
		self.log_config_file_name = log_config_file_name
		self.worker_list_string = ""
		for worker in self.worker_name_list:
			self.worker_list_string = self.worker_list_string + worker + " "			# This string will be used to pass the list as agrument


broker_name = "autobroker"											# Name of the broker
comm_type = "mpi"												# name of the core used
total_simulation_time = 0.10											# Simulation time that we are trying to reduce using parallelization


manager_name = "manager_1"
#worker_name_list = ["worker_A", "worker_B", "worker_C", "worker_D" , "worker_E", "worker_F"]
worker_name_list = ["worker_A", "worker_B", "worker_C"]
#worker_name_list = ["worker_A"]
log_config_file_name = "logger.json"



## Initialize the data structure
data = Structure(manager_name, worker_name_list, log_config_file_name)						



## configure the nodes
nodefile = os.environ["PBS_NODEFILE"]										# Requested node configuration using slurm is available in this file $PBS_NODEFILE
file_handle = open(nodefile,"r")										# Open the file
file_handle = file_handle.readlines()										# Read all the lines to a list. Contains extra server name alon with node name eg. abc.server.com
node_names = []													# A list to store the node names
for node in file_handle:											# Loop through the lines
	node_names.append(node.split(".")[0])									# split at "." and append only the first element that containes node name to node_names list



## configurations
num_federates = len(data.worker_name_list) + 1 + 1 								# num_worker + num_managers + num_loggers
if(len(node_names) < num_federates + 1):									# num_federates + broker
	print("requested wrong configuration")
	print("please request atleast 1 mpi job for broker; 1 mpi job for logger; 1 mpi job for manager and num_workers mpi jobs")
	sys.exit()



init_string = ""												# String that will be written to MPI config file				
counter = 0													# Variable to keep track of node in the node list

## Add Broker Initialization
init_string = init_string + "-np 1 --host {} python broker.py {} {} {}".format(node_names[counter], num_federates, broker_name, comm_type) + "\n" ; counter += 1

## Add Manager Initialization
init_string = init_string + "-np 1 --host {} python manager.py {} {} {}".format(node_names[counter], "./configuration/" + data.manager_name + ".json" , data.worker_list_string, total_simulation_time) + "\n"; counter += 1

## Add Worker Initialization
for file_name in data.worker_name_list:
	init_string = init_string + "-np 1 --host {} python worker.py {} {}".format(node_names[counter], "./configuration/" + file_name + ".json", data.manager_name) + "\n"; counter += 1

## Add Logger Initialization
init_string = init_string + "-np 1 --host {} python logger.py {}".format(node_names[counter], "./configuration/" + data.log_config_file_name) + "\n"; counter += 1

# Write the mpi config file
file = open("init-mpi.conf", "w")										# Write the Mpi config file which will be read by mpirun
file.write(init_string)
file.close()

mpi_runner = subprocess.call("mpirun --app init-mpi.conf", shell = True)					# Run the mpirun with the configuration file using a subprocess call 
print("Exit status: {}".format(mpi_runner))									# Returns after MPI finishes its job

