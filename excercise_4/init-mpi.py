import staff
import os
import subprocess

class Structure:
	def __init__(self, manager_name, worker_name_list, log_config_file_name):
		self.manager_name = manager_name
		self.worker_name_list = worker_name_list
		self.log_config_file_name = log_config_file_name
		self.worker_list_string = ""
		for worker in self.worker_name_list:
			self.worker_list_string = self.worker_list_string + worker + " "		

manager_name = "manager_1"
worker_name_list = ["worker_A", "worker_B", "worker_C", "worker_D" , "worker_E", "worker_F"]
log_config_file_name = "logger.json"


data = Structure(manager_name, worker_name_list, log_config_file_name)


num_federates = len(data.worker_name_list) + 1 + 1 						# num_worker + num_managers + num_loggers
broker_name = "autobroker"
comm_type = "mpi"

init_string = ""

## Add Broker Initialization
init_string = init_string + "-np 1 python broker.py {} {} {}".format(num_federates, broker_name, comm_type) + "\n"

## Add Manager Initialization
init_string = init_string + "-np 1 python manager.py {} {}".format("./configuration/" + data.manager_name + ".json" , data.worker_list_string) + "\n"

## Add Worker Initialization
for file_name in data.worker_name_list:
	init_string = init_string + "-np 1 python worker.py {} {}".format("./configuration/" + file_name + ".json", data.manager_name) + "\n"

## Add Logger Initialization
init_string = init_string + "-np 1 python logger.py {}".format("./configuration/" + data.log_config_file_name) + "\n"

print(init_string)

file = open("init-mpi.conf", "w")
file.write(init_string)
file.close()

mpi_runner = subprocess.call("mpirun --app init-mpi.conf", shell = True)
print("Exit status: {}".format(mpi_runner))

