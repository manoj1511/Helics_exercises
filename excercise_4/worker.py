import staff
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("worker_file_name", type = str)
parser.add_argument("manager_name", type = str)
args = parser.parse_args()
#print(args.worker_file_name)
#print(args.manager_name)

print("Strating Worker")
staff.init_worker(args.worker_file_name, args.manager_name)
