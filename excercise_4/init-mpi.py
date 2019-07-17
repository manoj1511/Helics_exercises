import staff
import os
import subprocess

class Structure:
	def __init__(self, manager_name, worker_name_list, log_config_file_name):
		self.manager_name = manager_name
		self.worker_name_list = worker_name_list
		self.log_config_file_name = log_config_file_name		

manager_name = "manager_1"
worker_name_list = ["worker_A"]
log_config_file_name = "logger.json"


data = Structure(manager_name, worker_name_list, log_config_file_name)



workers = []
num_federates = len(data.worker_name_list) + 1 + 1 						# num_worker + num_managers + oum_loggers
broker_name = "autobroker"


broker = subprocess.Popen("mpirun -np 1 python broker.py {} {}".format(num_federates, broker_name), shell = True)
manager = subprocess.Popen("mpirun -np 1 python manager.py {} {}".format("./configuration/" + data.manager_name + ".json" ,data.worker_name_list), shell=True)
for file_name in data.worker_name_list:
	workers.append(subprocess.Popen("mpirun -np 1 python worker.py {} {}".format("./configuration/" + file_name + ".json", data.manager_name), shell=True))
logger = subprocess.Popen("mpirun -np 1 python logger.py {}".format("./configuration/" + data.log_config_file_name), shell=True)


#broker = Process(target = staff.init_broker, args = (num_federates, broker_name))
#manager = Process(target = staff.init_manager, args = ("./configuration/" + data.manager_name + ".json", data.worker_name_list))
#for file_name in data.worker_name_list:
#	workers.append(Process(target = staff.init_worker, args = ("./configuration/" + file_name + ".json", data.manager_name)))
#logger = Process(target = staff.init_logger, args = ("./configuration/" + data.log_config_file_name,))



broker.wait()
manager.wait()
for worker in workers:
	worker.wait()
logger.wait()


