import staff
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("manager_config_file_name", type = str)
parser.add_argument("worker_list", type = str, nargs = "+")
args = parser.parse_args()
#print(args.manager_config_file_name)
#print("worker name list that is being passed to init_manager: {}".format(args.worker_list))
#print(args.worker_list)
#print(args.simulation_time)

print("Starting Manager as follows : staff.init_manager({},{})".format(args.manager_config_file_name, args.worker_list))
staff.init_manager(args.manager_config_file_name, args.worker_list)
