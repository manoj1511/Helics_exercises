import staff
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("logger_file_name", type = str)
parser.add_argument("log_out_file_name", type = str)
parser.add_argument("total_simulation_time", type = float)
parser.add_argument("individual_simulation_time", type = float)
args = parser.parse_args()
#print(args.logger_file_name)
print("Starting loger as follows : staff.init_logger({}, {}, {}, {})".format(args.logger_file_name, args.log_out_file_name, args.total_simulation_time, args.individual_simulation_time))
staff.init_logger(args.logger_file_name, args.log_out_file_name, args.total_simulation_time, args.individual_simulation_time)
