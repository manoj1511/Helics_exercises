import staff
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("manager_config_file_name", type = str)
parser.add_argument("worker_list", type = str, nargs = "+")
parser.add_argument("simulation_time", type = float)
args = parser.parse_args()
#print(args.manager_config_file_name)
#print("worker name list that is being passed to init_manager: {}".format(args.worker_list))
#print(args.worker_list)
#print(args.simulation_time)
print("Starting manager")
staff.init_manager(args.manager_config_file_name, args.worker_list, args.simulation_time)
