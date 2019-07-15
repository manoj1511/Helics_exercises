import staff
from multiprocessing import Process


class Structure:
	def __init__(self, manager_name, manager_config_file_name, worker_name_list, worker_config_file_list, log_config_file_name):
		self.manager_name = manager_name
		self.manager_config_file_name = manager_config_file_name
		self.worker_name_list = worker_name_list
		self.worker_config_file_list = worker_config_file_list
		self.log_config_file_name = log_config_file_name		



manager_name = "manager_1"
manager_config_file_name = "manager_1.json"
worker_name_list = ["worker_A","worker_B","worker_C"]
worker_config_file_list = ["worker_A.json","worker_B.json","worker_C.json"]
log_config_file_name = "logger.json"


data = Structure(manager_name, manager_config_file_name, worker_name_list, worker_config_file_list, log_config_file_name)



workers = []
num_federates = len(data.worker_name_list) + 1 + 1 						# num_worker + num_managers + oum_loggers
broker_name = "autobroker"


broker = Process(target = staff.init_broker, args = (num_federates, broker_name))
manager = Process(target = staff.init_manager, args = ("./configuration/" + data.manager_config_file_name, data.worker_name_list))
for file_name in data.worker_config_file_list:
	workers.append(Process(target = staff.init_worker, args = ("./configuration/" + file_name , data.manager_name)))
logger = Process(target = staff.init_logger, args = ("./configuration/" + data.log_config_file_name,))



broker.start()
manager.start()
for worker in workers:
	worker.start()
logger.start()



broker.join()
manager.join()
for worker in workers:
	worker.join()
logger.join()
