import staff
import subprocess

worker_name_list = ["abc", "def"]

manager_name = "manager_1"
manager_config_file_name = "./configuration/" + manager_name + ".json"
worker_str = ""
manager_config_file_name = "./configuration/manager_1.json"
print(manager_config_file_name)

for i in worker_name_list:
	worker_str = worker_str + i + " "

print(worker_str)
subprocess.Popen("mpirun -np 1 python manager.py {} {}".format(manager_config_file_name, worker_str), shell = True).wait()
